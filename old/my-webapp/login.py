from flask import Flask, render_template, request, redirect, url_for, session
import os
import pyotp
import json
from dotenv import load_dotenv
from SmartApi import SmartConnect
from logzero import logger

app = Flask(__name__)
app.secret_key = os.urandom(24)

ANGELALGO_PATH = r"C:\Users\user\projects\angelalgo"

def select_env_file():
    print("Select mode:")
    print("1. Trading")
    print("2. Historical Data")
    choice = input("Enter choice (1 or 2): ").strip()
    env_file = ".env.trading" if choice == "1" else ".env.historical"
    env_path = os.path.join(ANGELALGO_PATH, env_file)
    if load_dotenv(env_path):
        print(f"✅ {env_file} loaded successfully!")
    else:
        print(f"❌ Failed to load {env_file}!")
    return env_file

def login():
    try:
        select_env_file()
        
        API_KEY = os.getenv("API_KEY")
        CLIENT_ID = os.getenv("CLIENT_ID")
        PASSWORD = os.getenv("PASSWORD")
        TOTP_SECRET = os.getenv("SMARTAPI_TOTP_SECRET")
        
        if not all([API_KEY, CLIENT_ID, PASSWORD, TOTP_SECRET]):
            raise ValueError("Missing required environment variables!")
        
        totp = pyotp.TOTP(TOTP_SECRET).now()
        smart_api = SmartConnect(api_key=API_KEY)
        response = smart_api.generateSession(CLIENT_ID, PASSWORD, totp)
        
        if response["status"]:
            auth_token = response["data"]["jwtToken"]
            refresh_token = response["data"]["refreshToken"]
            
            token_path = os.path.join(ANGELALGO_PATH, "auth_token.json")
            with open(token_path, "w") as file:
                json.dump({"data": {"auth_token": auth_token, "client_id": CLIENT_ID}}, file)
            print(f"Auth token written to: {token_path}")
            
            logger.info("✅ Login Successful!")
            return smart_api, auth_token, refresh_token
        else:
            logger.error(f"❌ Login Failed: {response}")
            return None, None, None
    except Exception as e:
        logger.exception(f"Login error: {e}")
        return None, None, None

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        smart_api, auth_token, refresh_token = login()
        if smart_api:
            session['auth_token'] = auth_token
            return redirect(url_for('dashboard'))
        else:
            return "Login Failed", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'auth_token' not in session:
        return redirect(url_for('login_route'))
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)