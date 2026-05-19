"""
WebSocket Connection Test Script
Tests the collaborative coding WebSocket endpoint
"""

import asyncio
import websockets
import json
import sys


async def test_websocket_connection():
    """Test WebSocket connection to collaborative room"""

    # Configuration
    ROOM_CODE = "Z9GCNHQX"  # Replace with your room code from Postman test
    TOKEN = input("Enter your JWT token: ").strip()  # Get token from user

    if not TOKEN:
        print("❌ No token provided!")
        return False

    uri = f"ws://127.0.0.1:8000/ws/room/{ROOM_CODE}?token={TOKEN}"

    print(f"🔌 Attempting to connect to: {uri}")
    print("-" * 60)

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            print("-" * 60)

            # Wait for initial room_state message
            print("📥 Waiting for room_state message...")
            message = await websocket.recv()
            data = json.loads(message)
            print(f"✅ Received: {json.dumps(data, indent=2)}")
            print("-" * 60)

            # Send a ping
            print("📤 Sending ping...")
            await websocket.send(json.dumps({"type": "ping", "data": {}}))

            # Wait for pong
            print("📥 Waiting for pong...")
            response = await websocket.recv()
            pong_data = json.loads(response)
            print(f"✅ Received: {json.dumps(pong_data, indent=2)}")
            print("-" * 60)

            # Send a code change
            print("📤 Sending code change...")
            await websocket.send(
                json.dumps(
                    {
                        "type": "code_change",
                        "data": {
                            "code": "print('Hello from WebSocket!')",
                            "language": "python",
                        },
                    }
                )
            )
            print("✅ Code change sent!")
            print("-" * 60)

            # Send a chat message
            print("📤 Sending chat message...")
            await websocket.send(
                json.dumps(
                    {
                        "type": "chat_message",
                        "data": {"message": "Hello from test script!"},
                    }
                )
            )

            # Wait for broadcast
            print("📥 Waiting for chat broadcast...")
            chat_response = await websocket.recv()
            chat_data = json.loads(chat_response)
            print(f"✅ Received: {json.dumps(chat_data, indent=2)}")
            print("-" * 60)

            print("🎉 All tests passed!")
            print("✅ WebSocket connection is working correctly!")

    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Connection failed with status code: {e.status_code}")
        print(f"   This usually means authentication or authorization failed.")
        print(f"   Error: {e}")
        return False

    except ConnectionRefusedError:
        print("❌ Connection refused!")
        print("   Make sure the backend server is running on http://127.0.0.1:8000")
        return False

    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("WebSocket Connection Test")
    print("=" * 60)
    print()

    # Check if websockets is installed
    try:
        import websockets
    except ImportError:
        print("❌ websockets library not installed!")
        print("   Install it with: pip install websockets")
        sys.exit(1)

    # Run the test
    success = asyncio.run(test_websocket_connection())

    print()
    print("=" * 60)
    if success:
        print("✅ TEST PASSED")
    else:
        print("❌ TEST FAILED")
    print("=" * 60)

    sys.exit(0 if success else 1)
