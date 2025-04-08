import asyncio
import websockets
import json
from logzero import logger

async def live_stream(api_key, auth_token):
    uri = "wss://your.websocket.endpoint"  # Replace with your actual WebSocket endpoint
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"api_key": api_key, "auth_token": auth_token}))
        try:
            while True:
                response = await websocket.recv()
                logger.info(f"Received data: {response}")
                # Process the received data as needed
        except Exception as e:
            logger.exception(f"WebSocket error: {e}")

def start_live_stream(api_key, auth_token):
    asyncio.run(live_stream(api_key, auth_token))