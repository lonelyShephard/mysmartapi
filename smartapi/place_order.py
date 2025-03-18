import time
from logzero import logger
from login import login

def place_order():
    smart_api, auth_token, refresh_token = login()
    
    if smart_api:
        try:
            # Take user inputs for order details
            tradingsymbol = input("Enter stock symbol (e.g., SBIN-EQ): ").strip().upper()
            symboltoken = input("Enter stock token (e.g., 3045): ").strip()
            transactiontype = input("Enter transaction type (BUY/SELL): ").strip().upper()
            exchange = input("Enter exchange (NSE/BSE): ").strip().upper()
            ordertype = input("Enter order type (MARKET/LIMIT/SL/SLM): ").strip().upper()
            producttype = input("Enter product type (INTRADAY/DELIVERY): ").strip().upper()
            quantity = input("Enter quantity: ").strip()
            price = input("Enter price (leave empty for MARKET orders): ").strip() or "0"

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

            # Wait 10 seconds and check status again
            time.sleep(10)
            check_order_status(smart_api, order_id, delay=10)

            return order_id

        except Exception as e:
            logger.exception(f"❌ Order placement failed: {e}")

def check_order_status(smart_api, order_id, delay):
    try:
        # Fetch order book
        order_book = smart_api.orderBook()

        if order_book["status"]:
            for order in order_book["data"]:
                if order["orderid"] == order_id:
                    logger.info(f"🔍 [After {delay} sec] Order Found: {order}")
                    print(f"🆔 Order ID: {order['orderid']}")
                    print(f"🔹 Symbol: {order['tradingsymbol']} ({order['exchange']})")
                    print(f"📈 Order Type: {order['ordertype']}")
                    print(f"📊 Quantity: {order['quantity']} at Price: {order['price']}")
                    print(f"🕒 Status: {order['status']}")
                    return
            logger.warning(f"⚠️ [After {delay} sec] Order ID {order_id} not found.")
        else:
            logger.error("❌ Failed to fetch order book.")
    except Exception as e:
        logger.exception(f"❌ Error fetching order status: {e}")

if __name__ == "__main__":
    place_order()
