from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
import config

def on_data(wsapp, message):
    logger.info(f"📈 Market Data: {message}")

def on_open(wsapp):
    logger.info("✅ WebSocket Connected!")
    sws.subscribe("abc123", 1, [{"exchangeType": 1, "tokens": ["26009"]}])

def on_error(wsapp, error):
    logger.error(f"WebSocket Error: {error}")

def on_close(wsapp):
    logger.info("❌ WebSocket Disconnected!")

def start_websocket():
    sws = SmartWebSocketV2(config.API_KEY, config.CLIENT_ID, "authToken", "feedToken")
    
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    sws.connect()
