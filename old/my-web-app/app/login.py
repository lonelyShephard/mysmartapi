from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pyotp
import json
from dotenv import load_dotenv
from SmartApi import SmartConnect
from logzero import logger

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

ANGELALGO_PATH = r"C:\Users\user\projects\angelalgo"

def select_env_file():
    env_file = ".env.trading"
    env_path = os.path.join(ANGELALGO_PATH, env_file)
    if load_dotenv(env_path):
        logger.info(f"✅ {env_file} loaded successfully!")
    else:
        logger.error(f"❌ Failed to load {env_file}!")
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
            logger.info("✅ Login Successful!")
            return smart_api, auth_token, refresh_token
        else:
            logger.error(f"❌ Login Failed: {response}")
            return None, None, None
    except Exception as e:
        logger.exception(f"Login error: {e}")
        return None, None, None

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        smart_api, auth_token, refresh_token = login()
        if smart_api:
            return redirect(url_for('options'))
        else:
            flash('Login Failed. Please check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/options')
def options():
    return render_template('options.html')

if __name__ == "__main__":
    app.run(debug=True)