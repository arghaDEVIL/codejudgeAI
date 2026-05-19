"""
Test script for Docker-based code execution
Run this to verify Docker setup and execution
"""

from app.services.code_executor import code_executor
import json


def print_result(test_name: str, result: dict):
    """Pretty print test result"""
    print(f"\n{'=' * 60}")
    print(f"TEST: {test_name}")
    print(f"{'=' * 60}")
    print(json.dumps(result, indent=2))
    print(f"Status: {'✅ PASS' if result['status'] == 'Passed' else '❌ FAIL'}")


def main():
    print("\n🚀 Testing Docker-Based Code Execution\n")

    # Test 1: Simple Python
    print_result(
        "Python - Hello World",
        code_executor.execute(
            code='print("Hello, Docker!")',
            language="python",
            stdin="",
        ),
    )

    # Test 2: Python with stdin
    print_result(
        "Python - Read Input",
        code_executor.execute(
            code='name = input()\nprint(f"Hello, {name}!")',
            language="python",
            stdin="Alice",
        ),
    )

    # Test 3: Python - Time Limit
    print_result(
        "Python - Time Limit Exceeded",
        code_executor.execute(
            code="import time\ntime.sleep(5)",
            language="python",
            stdin="",
            time_limit=1000,  # 1 second
        ),
    )

    # Test 4: Python - Runtime Error
    print_result(
        "Python - Runtime Error",
        code_executor.execute(
            code="x = 1 / 0",
            language="python",
            stdin="",
        ),
    )

    # Test 5: Python - Memory Usage
    print_result(
        "Python - Memory Test",
        code_executor.execute(
            code="a = [i for i in range(1000000)]\nprint(len(a))",
            language="python",
            stdin="",
        ),
    )

    # Test 6: C++ - Hello World
    print_result(
        "C++ - Hello World",
        code_executor.execute(
            code='#include <iostream>\nint main() { std::cout << "Hello from C++!"; return 0; }',
            language="cpp",
            stdin="",
        ),
    )

    # Test 7: C++ - With Input
    print_result(
        "C++ - Read Input",
        code_executor.execute(
            code='#include <iostream>\n#include <string>\nint main() { std::string name; std::cin >> name; std::cout << "Hello, " << name << "!"; return 0; }',
            language="cpp",
            stdin="Bob",
        ),
    )

    # Test 8: C++ - Compilation Error
    print_result(
        "C++ - Compilation Error",
        code_executor.execute(
            code='#include <iostream>\nint main() { std::cout << "Missing semicolon" }',
            language="cpp",
            stdin="",
        ),
    )

    # Test 9: Python - Multiple Lines Output
    print_result(
        "Python - Multiple Lines",
        code_executor.execute(
            code="for i in range(5):\n    print(i)",
            language="python",
            stdin="",
        ),
    )

    # Test 10: Python - Math Operations
    print_result(
        "Python - Math Operations",
        code_executor.execute(
            code="a, b = map(int, input().split())\nprint(a + b)",
            language="python",
            stdin="10 20",
        ),
    )

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
