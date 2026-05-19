import asyncio
import websockets


async def test():
    uri = "ws://127.0.0.1:8000/ws/test"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as ws:
            print("✅ Connected!")
            msg = await ws.recv()
            print(f"Received: {msg}")
    except Exception as e:
        print(f"❌ Error: {e}")


asyncio.run(test())
