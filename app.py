from fetch_data import fetch_ltp, fetch_historical_data
from place_order import place_order
from websocket_stream import start_websocket

# Fetch LTP for Reliance
fetch_ltp("NSE", "RELIANCE", "2885")

# Fetch Historical Data
fetch_historical_data("NSE", "2885", "ONE_MINUTE", "2024-03-01 09:00", "2024-03-01 09:30")

# Place Order
place_order()

# Start WebSocket Streaming
start_websocket()
