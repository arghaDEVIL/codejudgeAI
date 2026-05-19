"""
Secure Docker-based code execution service
Provides isolated sandbox execution with resource limits
"""

import docker
import tempfile
import os
import time
import json
from typing import Dict, Optional
from docker.errors import DockerException, ContainerError, ImageNotFound
from pathlib import Path


class DockerExecutor:
    """
    Secure Docker-based code executor with resource limits

    Security Features:
    - Network isolation (no internet access)
    - Read-only filesystem (except /tmp)
    - CPU and memory limits
    - Execution timeout
    - No privileged access
    - Temporary file cleanup
    """

    # Docker images for each language
    IMAGES = {
        "python": "python:3.11-alpine",  # Lightweight Alpine-based image (~50MB)
        "cpp": "gcc:latest",  # Official GCC image (~1.2GB, includes g++)
    }

    # Default resource limits
    DEFAULT_TIME_LIMIT = 2000  # ms
    DEFAULT_MEMORY_LIMIT = 256  # MB
    DEFAULT_CPU_QUOTA = 100000  # 100% of one CPU core

    def __init__(self):
        """Initialize Docker client"""
        self.client = None
        self.available = None  # Lazy initialization
        self._initialized = False

    def _init_docker(self) -> bool:
        """Initialize and verify Docker availability (lazy)"""
        if self._initialized:
            return self.available

        self._initialized = True

        try:
            # Try different Docker connection methods for Windows compatibility
            try:
                # Method 1: TCP connection (works on your system)
                self.client = docker.DockerClient(base_url="tcp://localhost:2375")
            except Exception:
                try:
                    # Method 2: Default connection
                    self.client = docker.from_env()
                except Exception:
                    # Method 3: Named pipe for Windows Docker Desktop
                    self.client = docker.DockerClient(
                        base_url="npipe:////./pipe/docker_engine"
                    )

            # Test connection
            self.client.ping()
            print("✅ Docker is available for secure code execution")

            # Pull required images
            self._pull_images()
            self.available = True
            return True

        except DockerException as e:
            print(f"⚠️  Docker not available: {e}")
            print("⚠️  Falling back to subprocess mode")
            self.available = False
            return False
        except Exception as e:
            print(f"⚠️  Unexpected error initializing Docker: {e}")
            self.available = False
            return False

    def _pull_images(self):
        """Pull required Docker images if not present"""
        for lang, image in self.IMAGES.items():
            try:
                self.client.images.get(image)
                print(f"✅ Docker image '{image}' already available")
            except ImageNotFound:
                print(f"📥 Pulling Docker image '{image}'...")
                try:
                    self.client.images.pull(image)
                    print(f"✅ Successfully pulled '{image}'")
                except Exception as e:
                    print(f"❌ Failed to pull '{image}': {e}")

    def is_available(self) -> bool:
        """Check if Docker is available"""
        if not self._initialized:
            self._init_docker()
        return self.available and self.client is not None

    def execute(
        self,
        code: str,
        language: str,
        stdin: str = "",
        time_limit: int = None,
        memory_limit: int = None,
    ) -> Dict:
        """
        Execute code in Docker container

        Args:
            code: Source code to execute
            language: Programming language (python, cpp)
            stdin: Standard input for the program
            time_limit: Execution timeout in milliseconds
            memory_limit: Memory limit in MB

        Returns:
            {
                "status": str,  # Passed, Wrong Answer, TLE, RTE, CE, MLE
                "output": str,
                "error": str,
                "execution_time": int,  # milliseconds
                "memory_used": float,  # MB
                "exit_code": int
            }
        """
        if not self.is_available():
            return {
                "status": "RTE",
                "output": "",
                "error": "Docker not available",
                "execution_time": 0,
                "memory_used": 0,
                "exit_code": -1,
            }

        time_limit = time_limit or self.DEFAULT_TIME_LIMIT
        memory_limit = memory_limit or self.DEFAULT_MEMORY_LIMIT

        if language == "python":
            return self._execute_python(code, stdin, time_limit, memory_limit)
        elif language == "cpp":
            return self._execute_cpp(code, stdin, time_limit, memory_limit)
        else:
            return {
                "status": "RTE",
                "output": "",
                "error": f"Unsupported language: {language}",
                "execution_time": 0,
                "memory_used": 0,
                "exit_code": -1,
            }

    def _execute_python(
        self, code: str, stdin: str, time_limit: int, memory_limit: int
    ) -> Dict:
        """Execute Python code in Docker container"""

        # Create temporary directory for code
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write code to file
            code_file = os.path.join(tmpdir, "solution.py")
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)

            # Write stdin to file
            stdin_file = os.path.join(tmpdir, "input.txt")
            with open(stdin_file, "w", encoding="utf-8") as f:
                f.write(stdin)

            # Execute in container
            return self._run_container(
                image=self.IMAGES["python"],
                command=["python", "/code/solution.py"],
                tmpdir=tmpdir,
                stdin_file=stdin_file,
                time_limit=time_limit,
                memory_limit=memory_limit,
            )

    def _execute_cpp(
        self, code: str, stdin: str, time_limit: int, memory_limit: int
    ) -> Dict:
        """Execute C++ code in Docker container"""

        with tempfile.TemporaryDirectory() as tmpdir:
            # Write code to file
            code_file = os.path.join(tmpdir, "solution.cpp")
            with open(code_file, "w", encoding="utf-8") as f:
                f.write(code)

            # Write stdin to file
            stdin_file = os.path.join(tmpdir, "input.txt")
            with open(stdin_file, "w", encoding="utf-8") as f:
                f.write(stdin)

            # Step 1: Compile
            compile_result = self._compile_cpp(tmpdir, memory_limit)

            if compile_result["status"] == "CE":
                return compile_result

            # Step 2: Execute
            return self._run_container(
                image=self.IMAGES["cpp"],
                command=["/code/solution"],
                tmpdir=tmpdir,
                stdin_file=stdin_file,
                time_limit=time_limit,
                memory_limit=memory_limit,
            )

    def _compile_cpp(self, tmpdir: str, memory_limit: int) -> Dict:
        """Compile C++ code in Docker container"""
        try:
            container = self.client.containers.run(
                image=self.IMAGES["cpp"],
                command=[
                    "g++",
                    "/code/solution.cpp",
                    "-o",
                    "/code/solution",
                    "-std=c++17",
                    "-O2",
                ],
                volumes={tmpdir: {"bind": "/code", "mode": "rw"}},
                mem_limit=f"{memory_limit}m",
                network_disabled=True,
                detach=False,
                remove=True,
                stdout=True,
                stderr=True,
            )

            return {"status": "OK"}

        except ContainerError as e:
            return {
                "status": "CE",
                "output": "",
                "error": e.stderr.decode("utf-8") if e.stderr else str(e),
                "execution_time": 0,
                "memory_used": 0,
                "exit_code": e.exit_status,
            }
        except Exception as e:
            return {
                "status": "CE",
                "output": "",
                "error": f"Compilation error: {str(e)}",
                "execution_time": 0,
                "memory_used": 0,
                "exit_code": -1,
            }

    def _run_container(
        self,
        image: str,
        command: list,
        tmpdir: str,
        stdin_file: str,
        time_limit: int,
        memory_limit: int,
    ) -> Dict:
        """Run code in Docker container with resource limits"""

        container = None
        start_time = time.time()

        try:
            # Container configuration
            container_config = {
                "image": image,
                "command": f"sh -c 'cat /code/input.txt | {' '.join(command)}'",
                "volumes": {tmpdir: {"bind": "/code", "mode": "ro"}},
                "working_dir": "/code",
                "detach": True,
                "remove": False,  # Don't auto-remove so we can get stats
                # Security settings
                "network_disabled": True,  # No internet access
                "read_only": True,  # Read-only filesystem
                "tmpfs": {"/tmp": "size=10m"},  # Small writable /tmp
                # Resource limits
                "mem_limit": f"{memory_limit}m",
                "memswap_limit": f"{memory_limit}m",  # Disable swap
                "cpu_quota": self.DEFAULT_CPU_QUOTA,
                "cpu_period": 100000,
                "pids_limit": 50,  # Limit number of processes
                # Additional security
                "cap_drop": ["ALL"],  # Drop all capabilities
                "security_opt": ["no-new-privileges"],
            }

            # Create and start container
            container = self.client.containers.run(**container_config)

            # Wait for completion with timeout
            timeout_seconds = time_limit / 1000
            exit_code = container.wait(timeout=timeout_seconds)["StatusCode"]

            execution_time = int((time.time() - start_time) * 1000)

            # Get output
            logs = container.logs(stdout=True, stderr=True).decode("utf-8")

            # Split stdout and stderr (Docker combines them)
            output_lines = []
            error_lines = []

            for line in logs.split("\n"):
                if line.strip():
                    output_lines.append(line)

            output = "\n".join(output_lines)
            error = ""

            # Get memory stats
            try:
                stats = container.stats(stream=False)
                memory_used = stats["memory_stats"].get("max_usage", 0) / (1024 * 1024)

                # Check for memory limit exceeded
                if memory_used >= memory_limit * 0.95:  # 95% threshold
                    status = "MLE"
                    error = "Memory limit exceeded"
                elif exit_code == 0:
                    status = "Passed"
                elif exit_code == 137:  # SIGKILL (OOM or timeout)
                    status = "MLE"
                    error = "Memory limit exceeded or killed"
                else:
                    status = "RTE"
                    error = f"Runtime error (exit code: {exit_code})"

            except Exception:
                memory_used = 0
                status = "RTE" if exit_code != 0 else "Passed"

            return {
                "status": status,
                "output": output.strip(),
                "error": error.strip(),
                "execution_time": execution_time,
                "memory_used": round(memory_used, 2),
                "exit_code": exit_code,
            }

        except docker.errors.APIError as e:
            if "timeout" in str(e).lower() or "read timed out" in str(e).lower():
                return {
                    "status": "TLE",
                    "output": "",
                    "error": "Time limit exceeded",
                    "execution_time": time_limit,
                    "memory_used": 0,
                    "exit_code": -1,
                }
            else:
                return {
                    "status": "RTE",
                    "output": "",
                    "error": f"Container error: {str(e)}",
                    "execution_time": int((time.time() - start_time) * 1000),
                    "memory_used": 0,
                    "exit_code": -1,
                }

        except Exception as e:
            if "timeout" in str(e).lower() or "read timed out" in str(e).lower():
                return {
                    "status": "TLE",
                    "output": "",
                    "error": "Time limit exceeded",
                    "execution_time": time_limit,
                    "memory_used": 0,
                    "exit_code": -1,
                }
            else:
                return {
                    "status": "RTE",
                    "output": "",
                    "error": f"Execution error: {str(e)}",
                    "execution_time": int((time.time() - start_time) * 1000),
                    "memory_used": 0,
                    "exit_code": -1,
                }

        finally:
            # Cleanup container
            if container:
                try:
                    container.stop(timeout=1)
                    container.remove()
                except Exception:
                    pass


# Global instance
docker_executor = DockerExecutor()
