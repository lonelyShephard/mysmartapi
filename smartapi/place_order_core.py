import json
import time
from smartapi.login import login
from logzero import logger
from flask import session

# Load stock symbols from stocks.json.
def load_stocks(json_file):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)

        # Create dictionary {symbol: {token, exchange}}
        stock_dict = {entry["symbol"]: {"token": entry["token"], "exchange": entry["exchange"]} for entry in data}
        return stock_dict

    except Exception as e:
        print(f"❌ Error loading stocks: {e}")
        return {}

# Load stock data
stock_dict = load_stocks("stocks.json")

# Place order function
def place_order(tradingsymbol, symboltoken, transactiontype, exchange, ordertype, producttype, quantity, price):
    smart_api, auth_token, refresh_token = login()
    
    if smart_api:
        try:
            if not symboltoken:
                logger.error("Invalid stock selection!")
                return

            # Define order parameters
            order_params = {
                "variety": "NORMAL",
                "tradingsymbol": tradingsymbol,
                "symboltoken": symboltoken,
                "transactiontype": transactiontype,
                "exchange": exchange,
                "ordertype": ordertype,
                "producttype": producttype,
                "duration": "DAY",
                "price": price,
                "squareoff": "0",
                "stoploss": "0",
                "quantity": quantity
            }

            # Place order
            order_id = smart_api.placeOrder(order_params)
            logger.info(f"✅ Order Placed! Order ID: {order_id}")

            # Check order status immediately
            check_order_status(smart_api, order_id, delay=0)

            # Schedule a second check after 10 seconds
            # root.after(10000, lambda: check_order_status(smart_api, order_id, delay=30))

        except Exception as e:
            logger.exception(f"❌ Order placement failed: {e}")

# Function to check order status
def check_order_status(smart_api, order_id, delay):
    try:
        order_book = smart_api.orderBook()
        if order_book["status"]:
            for order in order_book["data"]:
                if order["orderid"] == order_id:
                    status_message = f"[After {delay} sec] Order {order_id} Status: {order['status']}"
                    logger.info(status_message)
                    return
        logger.info(f"⚠️ Order {order_id} not found.")
    except Exception as e:
        logger.exception(f"❌ Error fetching order status: {e}")
