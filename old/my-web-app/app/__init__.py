from flask import Flask

app = Flask(__name__)

from app import login, options, fetch_data_gui, place_order_gui, websocket_stream, exit_smartapi

# Additional application setup code can be added here if needed.