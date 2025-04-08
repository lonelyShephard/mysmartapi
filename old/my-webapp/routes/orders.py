from flask import Blueprint, request, jsonify
from SmartApi import SmartConnect
from logzero import logger
import json
import os

orders_bp = Blueprint('orders', __name__)

ANGELALGO_PATH = r"C:\Users\user\projects\angelalgo"

@orders_bp.route('/place_order', methods=['POST'])
def place_order():
    try:
        data = request.json
        auth_token = data.get('auth_token')
        client_id = data.get('client_id')
        
        if not auth_token or not client_id:
            return jsonify({"error": "Missing auth_token or client_id"}), 400
        
        smart_api = SmartConnect(api_key=os.getenv("API_KEY"))
        smart_api.setAuthToken(auth_token)
        
        order_response = smart_api.placeOrder(
            orderType=data.get('order_type'),
            quantity=data.get('quantity'),
            price=data.get('price'),
            symbol=data.get('symbol'),
            transactionType=data.get('transaction_type')
        )
        
        if order_response["status"]:
            return jsonify({"message": "Order placed successfully!", "data": order_response["data"]}), 200
        else:
            logger.error(f"❌ Order placement failed: {order_response}")
            return jsonify({"error": "Order placement failed", "details": order_response}), 400
            
    except Exception as e:
        logger.exception(f"Order placement error: {e}")
        return jsonify({"error": "An error occurred while placing the order"}), 500