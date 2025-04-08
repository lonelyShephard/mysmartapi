# smartapi/__init__.py

from .config import API_KEY, CLIENT_ID, PASSWORD, TOTP_SECRET
from .login import login #changed this line
from .fetch_data_core import fetch_ltp, fetch_historical_data
from .place_order_core import place_order  # assuming you expose a function for order placement
from .websocket_stream import start_websocket  # for live streaming #changed this line
from .exit_smartapi import logout  # for exit functionality #changed this line

__all__ = ["login", "fetch_ltp", "fetch_historical_data", "place_order", "start_websocket", "logout"] #changed this line
