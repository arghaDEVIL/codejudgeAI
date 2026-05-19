# Docker-Based Code Execution Guide

## Overview

The code judge platform now uses **Docker containers** for secure, isolated code execution with strict resource limits. This provides:

- **Security**: Network isolation, read-only filesystem, no privileged access
- **Resource Control**: CPU, memory, and time limits
- **Isolation**: Each submission runs in a fresh container
- **Consistency**: Same environment across all executions

## Architecture

```
User Submission → FastAPI → CodeExecutor → DockerExecutor → Docker Container
                                    ↓
                              SubprocessExecutor (fallback)
```

### Components

1. **docker_executor.py**: Secure Docker-based execution engine
2. **code_executor.py**: Main executor with automatic fallback
3. **Docker Images**: Lightweight Alpine-based images

## Docker Images Used

### Python
- **Image**: `python:3.11-alpine`
- **Size**: ~50MB (vs 900MB for standard python image)
- **Features**: Python 3.11, pip, standard library

### C++
- **Image**: `gcc:12-alpine`
- **Size**: ~200MB (vs 1.2GB for standard gcc image)
- **Features**: GCC 12, g++, C++17 support

### Why Alpine?
- Minimal attack surface
- Faster pull and startup times
- Lower memory footprint
- Production-ready

## Security Features

### 1. Network Isolation
```python
network_disabled=True
```
- No internet access
- Cannot make external API calls
- Cannot download malicious code

### 2. Read-Only Filesystem
```python
read_only=True
tmpfs={"/tmp": "size=10m"}
```
- Code cannot modify system files
- Only /tmp is writable (10MB limit)
- Prevents persistence attacks

### 3. Resource Limits
```python
mem_limit="256m"
memswap_limit="256m"  # Disable swap
cpu_quota=100000      # 100% of one core
pids_limit=50         # Max 50 processes
```

### 4. Capability Dropping
```python
cap_drop=["ALL"]
security_opt=["no-new-privileges"]
```
- Removes all Linux capabilities
- Prevents privilege escalation
- No raw socket access
- No system administration

### 5. Automatic Cleanup
- Containers are removed after execution
- Temporary files are deleted
- No resource leaks

## Resource Limits

### Default Limits
- **Time**: 2000ms (2 seconds)
- **Memory**: 256MB
- **CPU**: 100% of one core
- **Processes**: 50 max
- **Disk**: 10MB in /tmp

### Customizable Per Problem
```python
code_executor.execute(
    code=code,
    language="python",
    stdin=input_data,
    time_limit=5000,    # 5 seconds
    memory_limit=512,   # 512 MB
)
```

## Verdict Types

| Verdict | Code | Description |
|---------|------|-------------|
| Passed | `Passed` | Execution successful, exit code 0 |
| Wrong Answer | `WA` | Output doesn't match expected |
| Time Limit Exceeded | `TLE` | Execution timeout |
| Memory Limit Exceeded | `MLE` | Memory usage > 95% of limit |
| Runtime Error | `RTE` | Non-zero exit code or crash |
| Compilation Error | `CE` | C++ compilation failed |

## Installation & Setup

### Windows (Development)

1. **Install Docker Desktop**
   ```bash
   # Download from: https://www.docker.com/products/docker-desktop
   # Enable WSL 2 backend for better performance
   ```

2. **Verify Installation**
   ```bash
   docker --version
   docker run hello-world
   ```

3. **Pull Required Images**
   ```bash
   docker pull python:3.11-alpine
   docker pull gcc:12-alpine
   ```

4. **Start Backend**
   ```bash
   cd backend
   python run.py
   ```
   
   You should see:
   ```
   ✅ Docker is available for secure code execution
   ✅ Docker image 'python:3.11-alpine' already available
   ✅ Docker image 'gcc:12-alpine' already available
   ✅ Using Docker for code execution
   ```

### Linux (Production)

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

2. **Enable Docker Service**
   ```bash
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

3. **Pull Images**
   ```bash
   docker pull python:3.11-alpine
   docker pull gcc:12-alpine
   ```

### macOS

1. **Install Docker Desktop**
   ```bash
   brew install --cask docker
   ```

2. **Start Docker Desktop** from Applications

3. **Pull Images** (same as above)

## Fallback Mode

If Docker is not available, the system automatically falls back to subprocess execution:

```
⚠️  Docker not available: Cannot connect to the Docker daemon
⚠️  Using subprocess fallback for code execution
```

### Fallback Limitations
- No network isolation
- No memory tracking
- Limited resource control (Windows)
- Less secure

### When Fallback is Used
- Docker not installed
- Docker daemon not running
- Permission issues
- Development without Docker

## Testing Docker Execution

### Test Python Execution
```python
from app.services.code_executor import code_executor

result = code_executor.execute(
    code='print("Hello, Docker!")',
    language="python",
    stdin="",
)

print(result)
# {
#     "status": "Passed",
#     "output": "Hello, Docker!",
#     "error": "",
#     "execution_time": 150,
#     "memory_used": 8.5,
#     "exit_code": 0
# }
```

### Test C++ Execution
```python
result = code_executor.execute(
    code='#include <iostream>\nint main() { std::cout << "Hello!"; }',
    language="cpp",
    stdin="",
)
```

### Test Resource Limits
```python
# Test timeout
result = code_executor.execute(
    code='import time; time.sleep(10)',
    language="python",
    time_limit=1000,  # 1 second
)
# Expected: {"status": "TLE", ...}

# Test memory limit
result = code_executor.execute(
    code='a = [0] * (10**9)',  # Try to allocate 8GB
    language="python",
    memory_limit=256,  # 256MB
)
# Expected: {"status": "MLE", ...}
```

## Performance Considerations

### Container Startup Time
- **First run**: ~2-3 seconds (image pull)
- **Subsequent runs**: ~200-500ms (cached)
- **Alpine images**: Faster than standard images

### Optimization Tips
1. **Pre-pull images** during deployment
2. **Use Alpine** variants for smaller size
3. **Keep containers running** for batch jobs (future)
4. **Monitor Docker daemon** resource usage

## Monitoring & Debugging

### Check Docker Status
```bash
docker ps -a                    # List all containers
docker images                   # List images
docker stats                    # Resource usage
docker system df                # Disk usage
```

### View Logs
```bash
# Backend logs show execution details
tail -f backend.log

# Docker daemon logs
journalctl -u docker -f         # Linux
```

### Common Issues

#### 1. "Docker not available"
**Solution**: Start Docker Desktop or daemon
```bash
# Windows: Start Docker Desktop
# Linux: sudo systemctl start docker
# macOS: Open Docker Desktop
```

#### 2. "Permission denied"
**Solution**: Add user to docker group
```bash
sudo usermod -aG docker $USER
# Logout and login again
```

#### 3. "Image not found"
**Solution**: Pull images manually
```bash
docker pull python:3.11-alpine
docker pull gcc:12-alpine
```

#### 4. Slow execution
**Solution**: 
- Check Docker Desktop resources (CPU/Memory)
- Increase allocated resources in settings
- Use WSL 2 backend on Windows

## Production Deployment

### Docker Compose Setup
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock  # Docker socket
    environment:
      - DOCKER_ENABLED=true
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 4G
```

### Security Hardening
1. **Use Docker socket proxy** (don't expose directly)
2. **Run backend as non-root** user
3. **Enable AppArmor/SELinux** profiles
4. **Regular image updates** for security patches
5. **Monitor container escapes** with audit logs

### Scaling
- **Horizontal**: Multiple backend instances
- **Vertical**: Increase Docker daemon resources
- **Queue-based**: Use Celery for async execution
- **Kubernetes**: For large-scale deployments

## Future Enhancements

1. **More Languages**: Java, JavaScript, Go, Rust
2. **Custom Images**: Per-problem Docker images
3. **GPU Support**: For ML/AI problems
4. **Distributed Execution**: Multiple Docker hosts
5. **Container Pooling**: Reuse containers for speed
6. **Advanced Metrics**: CPU cycles, syscalls, I/O

## Best Practices

### For Developers
- Always test with Docker enabled
- Handle both Docker and subprocess modes
- Set appropriate resource limits per problem
- Clean up temporary files
- Log execution metrics

### For System Administrators
- Monitor Docker daemon health
- Set up log rotation
- Regular security updates
- Backup container configurations
- Implement rate limiting

### For Problem Setters
- Test problems with resource limits
- Provide reasonable time/memory limits
- Consider edge cases (infinite loops, memory bombs)
- Document expected resource usage

## References

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Alpine Linux](https://alpinelinux.org/)
- [Docker Python SDK](https://docker-py.readthedocs.io/)
- [Container Security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

## Support

For issues or questions:
1. Check Docker daemon status
2. Review backend logs
3. Test with simple code first
4. Verify image availability
5. Check resource limits

---

**Status**: ✅ Production Ready
**Last Updated**: 2026-04-15
**Version**: 1.0.0
