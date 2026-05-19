# Quick Docker Setup Guide

## For Windows Users

### Step 1: Install Docker Desktop

1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Run the installer
3. Enable WSL 2 during installation (recommended for better performance)
4. Restart your computer if prompted

### Step 2: Start Docker Desktop

1. Open Docker Desktop from Start Menu
2. Wait for Docker to start (whale icon in system tray should be steady)
3. You may need to accept the service agreement

### Step 3: Verify Docker Installation

Open PowerShell or Command Prompt and run:

```bash
docker --version
```

Expected output:
```
Docker version 24.0.x, build xxxxx
```

Test Docker:
```bash
docker run hello-world
```

You should see "Hello from Docker!" message.

### Step 4: Pull Required Images

```bash
docker pull python:3.11-alpine
docker pull gcc:12-alpine
```

This will download the lightweight images needed for code execution (~250MB total).

### Step 5: Start Your Backend

```bash
cd backend
python run.py
```

Look for these messages:
```
✅ Docker is available for secure code execution
✅ Docker image 'python:3.11-alpine' already available
✅ Docker image 'gcc:12-alpine' already available
✅ Using Docker for code execution
```

### Step 6: Test Execution

```bash
python test_docker_execution.py
```

You should see multiple tests passing with Docker execution.

## Troubleshooting

### "Docker daemon is not running"

**Solution**: Start Docker Desktop from Start Menu

### "Access denied" or "Permission error"

**Solution**: 
1. Make sure Docker Desktop is running
2. Run PowerShell/CMD as Administrator
3. Or add your user to docker-users group:
   - Open Computer Management
   - Go to Local Users and Groups > Groups
   - Double-click "docker-users"
   - Add your user account
   - Logout and login again

### "WSL 2 installation is incomplete"

**Solution**:
1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart computer
4. Start Docker Desktop again

### Images taking too long to download

**Solution**:
- Be patient, first download takes time
- Check your internet connection
- Images are cached after first download

### "Cannot connect to Docker daemon"

**Solution**:
1. Check if Docker Desktop is running (whale icon in system tray)
2. Restart Docker Desktop
3. Restart your computer
4. Reinstall Docker Desktop if issue persists

## Verification Checklist

- [ ] Docker Desktop installed
- [ ] Docker Desktop running (whale icon steady)
- [ ] `docker --version` works
- [ ] `docker run hello-world` works
- [ ] Python image pulled: `docker images | grep python`
- [ ] GCC image pulled: `docker images | grep gcc`
- [ ] Backend starts with "✅ Using Docker for code execution"
- [ ] Test script passes: `python test_docker_execution.py`

## Performance Tips

### Increase Docker Resources

1. Open Docker Desktop
2. Go to Settings > Resources
3. Increase:
   - CPUs: 4 or more
   - Memory: 4GB or more
   - Disk: 20GB or more
4. Click "Apply & Restart"

### Use WSL 2 Backend

1. Open Docker Desktop
2. Go to Settings > General
3. Enable "Use the WSL 2 based engine"
4. Click "Apply & Restart"

This provides better performance on Windows.

## Next Steps

Once Docker is working:

1. ✅ Submit code on the Judge page
2. ✅ Code runs in secure Docker containers
3. ✅ View execution results with metrics
4. ✅ Check AI feedback for improvements

## Need Help?

- Docker Documentation: https://docs.docker.com/desktop/windows/
- Docker Forums: https://forums.docker.com/
- WSL 2 Guide: https://docs.microsoft.com/en-us/windows/wsl/install

---

**Happy Coding! 🚀**
