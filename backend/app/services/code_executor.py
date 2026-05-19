"""
Code execution service with Docker sandbox support
Falls back to subprocess if Docker is not available
Cross-platform compatible (Windows, Linux, macOS)
"""

import subprocess
import tempfile
import os
import time
from typing import Dict, Optional

# Import Docker executor
from app.services.docker_executor import docker_executor

# Conditional import for Unix-only resource module
try:
    import resource

    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False
    print(
        "⚠️  'resource' module not available (Windows). Resource limits disabled in subprocess mode."
    )


class CodeExecutor:
    """
    Execute code safely with Docker or subprocess fallback

    Priority:
    1. Docker (secure, isolated, resource-limited)
    2. Subprocess (fallback for development)
    """

    def __init__(self):
        self.use_docker = docker_executor.is_available()
        if self.use_docker:
            print("✅ Using Docker for code execution")
        else:
            print("⚠️  Using subprocess fallback for code execution")

    def execute(
        self,
        code: str,
        language: str,
        stdin: str = "",
        time_limit: int = 2000,  # milliseconds
        memory_limit: int = 256,  # MB
    ) -> Dict:
        """
        Execute code and return result

        Returns:
            {
                "status": "Passed" | "Wrong Answer" | "TLE" | "RTE" | "CE" | "MLE",
                "output": str,
                "error": str,
                "execution_time": int (ms),
                "memory_used": float (MB),
                "exit_code": int
            }
        """
        if self.use_docker:
            return docker_executor.execute(
                code, language, stdin, time_limit, memory_limit
            )
        else:
            return self._execute_subprocess(
                code, language, stdin, time_limit, memory_limit
            )

    def _execute_subprocess(
        self, code: str, language: str, stdin: str, time_limit: int, memory_limit: int
    ) -> Dict:
        """Execute code using subprocess (fallback)"""
        try:
            start_time = time.time()

            if language == "python":
                result = self._execute_python_subprocess(code, stdin, time_limit)
            elif language == "cpp":
                result = self._execute_cpp_subprocess(code, stdin, time_limit)
            else:
                return {
                    "status": "RTE",
                    "output": "",
                    "error": f"Unsupported language: {language}",
                    "execution_time": 0,
                    "memory_used": 0,
                    "exit_code": -1,
                }

            execution_time = int((time.time() - start_time) * 1000)
            result["execution_time"] = execution_time

            return result

        except subprocess.TimeoutExpired:
            return {
                "status": "TLE",
                "output": "",
                "error": "Time limit exceeded",
                "execution_time": time_limit,
                "memory_used": 0,
                "exit_code": -1,
            }
        except Exception as e:
            return {
                "status": "RTE",
                "output": "",
                "error": str(e),
                "execution_time": 0,
                "memory_used": 0,
                "exit_code": -1,
            }

    def _execute_python_subprocess(
        self, code: str, stdin: str, time_limit: int
    ) -> Dict:
        """Execute Python code"""
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".py", mode="w", encoding="utf-8"
        ) as f:
            f.write(code)
            source_file = f.name

        try:
            result = subprocess.run(
                ["python", source_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=time_limit / 1000,
            )

            os.unlink(source_file)

            if result.returncode == 0:
                status = "Passed"
            else:
                status = "RTE"

            return {
                "status": status,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "memory_used": 0,  # Not tracked in subprocess mode
                "exit_code": result.returncode,
            }
        finally:
            if os.path.exists(source_file):
                os.unlink(source_file)

    def _execute_cpp_subprocess(self, code: str, stdin: str, time_limit: int) -> Dict:
        """Execute C++ code"""
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".cpp", mode="w", encoding="utf-8"
        ) as f:
            f.write(code)
            source_file = f.name

        exe_file = source_file.replace(".cpp", ".exe" if os.name == "nt" else "")

        try:
            # Compile
            compile_result = subprocess.run(
                ["g++", source_file, "-o", exe_file, "-std=c++17"],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if compile_result.returncode != 0:
                return {
                    "status": "CE",
                    "output": "",
                    "error": compile_result.stderr.strip(),
                    "memory_used": 0,
                    "exit_code": compile_result.returncode,
                }

            # Run
            run_result = subprocess.run(
                [exe_file],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=time_limit / 1000,
            )

            if run_result.returncode == 0:
                status = "Passed"
            else:
                status = "RTE"

            return {
                "status": status,
                "output": run_result.stdout.strip(),
                "error": run_result.stderr.strip(),
                "memory_used": 0,
                "exit_code": run_result.returncode,
            }

        finally:
            if os.path.exists(source_file):
                os.unlink(source_file)
            if os.path.exists(exe_file):
                os.unlink(exe_file)


# Global executor instance
code_executor = CodeExecutor()
