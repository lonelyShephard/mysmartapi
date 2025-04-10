import os
from flask import Flask, render_template, request, redirect, url_for, session
from smartapi import login, fetch_ltp, fetch_historical_data, place_order, start_websocket, logout
from smartapi.config import API_KEY, CLIENT_ID, PASSWORD, TOTP_SECRET
from logzero import logger

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

# Load default values from .env.trading
def load_default_env():
    default_env = {}
    with open(".env.trading", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            default_env[key] = value
    return default_env

default_env = load_default_env()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form.get("api_key")
        client_id = request.form.get("client_id")
        password = request.form.get("password")
        totp_secret = request.form.get("totp_secret")

        # Store credentials in session
        session["api_key"] = api_key
        session["client_id"] = client_id
        session["password"] = password
        session["totp_secret"] = totp_secret

        smart_api, auth_token, refresh_token = login()
        if smart_api:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="Login failed!", default_env=default_env)

    return render_template("index.html", default_env=default_env)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    return render_template("dashboard.html")

@app.route("/trading", methods=["GET", "POST"])
def trading():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    if request.method == "POST":
        # Get form data
        tradingsymbol = request.form.get("symbol")
        symboltoken = request.form.get("token")
        transactiontype = request.form.get("transaction")
        exchange = request.form.get("exchange")
        ordertype = request.form.get("order_type")
        producttype = request.form.get("product_type")
        quantity = request.form.get("quantity")
        price = request.form.get("price")

        place_order(tradingsymbol, symboltoken, transactiontype, exchange, ordertype, producttype, quantity, price)
        return render_template("trading.html", message="Order Placed!")
    return render_template("trading.html")

@app.route("/historical", methods=["GET", "POST"])
def historical():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    if request.method == "POST":
        # Get form data
        symbol = request.form.get("symbol")
        token = request.form.get("token")
        exchange = request.form.get("exchange")
        interval = request.form.get("interval")
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        from_time = request.form.get("from_time")
        to_time = request.form.get("to_time")

        fetch_historical_data(symbol, token, exchange, interval, from_date, to_date, from_time, to_time)
        return render_template("historical.html", message="Historical Data Fetched!")
    return render_template("historical.html")

@app.route("/streaming")
def streaming():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    start_websocket()
    return render_template("streaming.html")

@app.route("/logout")
def logout_route():
    if session.get("logged_in"):
        logout()
        session.clear()
        return redirect(url_for("index"))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
