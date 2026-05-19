"""
Simple Docker connection test to diagnose the issue
"""

import docker
from docker.errors import DockerException


def test_docker_connections():
    """Test different Docker connection methods"""

    print("🔍 Testing Docker connections...\n")

    # Test 1: Default connection
    print("1️⃣ Testing default connection (docker.from_env())...")
    try:
        client = docker.from_env()
        client.ping()
        print("✅ Default connection works!")
        return client
    except Exception as e:
        print(f"❌ Default connection failed: {e}")

    # Test 2: Named pipe (Windows Docker Desktop)
    print("\n2️⃣ Testing named pipe connection...")
    try:
        client = docker.DockerClient(base_url="npipe:////./pipe/docker_engine")
        client.ping()
        print("✅ Named pipe connection works!")
        return client
    except Exception as e:
        print(f"❌ Named pipe connection failed: {e}")

    # Test 3: TCP connection (if enabled)
    print("\n3️⃣ Testing TCP connection...")
    try:
        client = docker.DockerClient(base_url="tcp://localhost:2375")
        client.ping()
        print("✅ TCP connection works!")
        return client
    except Exception as e:
        print(f"❌ TCP connection failed: {e}")

    # Test 4: Check Docker Desktop status
    print("\n4️⃣ Checking Docker Desktop status...")
    import subprocess

    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker CLI available: {result.stdout.strip()}")
        else:
            print(f"❌ Docker CLI failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Docker CLI test failed: {e}")

    try:
        result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker daemon is responding to CLI")
        else:
            print(f"❌ Docker daemon not responding: {result.stderr}")
    except Exception as e:
        print(f"❌ Docker ps test failed: {e}")

    print("\n❌ All Docker connection methods failed!")
    return None


def test_docker_images(client):
    """Test Docker images"""
    if not client:
        return

    print("\n📦 Testing Docker images...")
    try:
        images = client.images.list()
        print(f"✅ Found {len(images)} Docker images")

        for image in images:
            if image.tags:
                for tag in image.tags:
                    if "python" in tag or "gcc" in tag:
                        print(f"  📋 {tag}")
    except Exception as e:
        print(f"❌ Failed to list images: {e}")


if __name__ == "__main__":
    client = test_docker_connections()
    test_docker_images(client)

    print("\n" + "=" * 60)
    if client:
        print("✅ Docker is working! The issue might be in the code.")
    else:
        print("❌ Docker connection failed. Possible solutions:")
        print("   1. Make sure Docker Desktop is running")
        print("   2. Restart Docker Desktop")
        print("   3. Enable 'Expose daemon on tcp://localhost:2375' in Docker settings")
        print("   4. Check Windows Docker Desktop troubleshooting")
    print("=" * 60)
