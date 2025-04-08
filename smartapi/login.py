import os
import pyotp
import json
from dotenv import load_dotenv
from SmartApi import SmartConnect
from logzero import logger
from flask import session

# Set the path for the angelweb directory
ANGELWEB_PATH = r"C:\Users\user\projects\angelweb"

def load_trading_env():
    """Loads the .env.trading environment file."""
    env_file = ".env.trading"
    env_path = os.path.join(ANGELWEB_PATH, env_file)
    if load_dotenv(env_path):
        logger.info(f"✅ {env_file} loaded successfully!")
    else:
        logger.error(f"❌ Failed to load {env_file}!")
    return env_file

def login():
    try:
        load_trading_env()  # Always load the trading environment
        
        API_KEY = session.get("api_key")
        CLIENT_ID = session.get("client_id")
        PASSWORD = session.get("password")
        TOTP_SECRET = session.get("totp_secret")
        
        if not all([API_KEY, CLIENT_ID, PASSWORD, TOTP_SECRET]):
            raise ValueError("Missing required environment variables!")
        
        totp = pyotp.TOTP(TOTP_SECRET).now() #generate totp using the secret
        smart_api = SmartConnect(api_key=API_KEY)
        response = smart_api.generateSession(CLIENT_ID, PASSWORD, totp)
        
        if response["status"]:
            auth_token = response["data"]["jwtToken"]
            refresh_token = response["data"]["refreshToken"]
            
            # Write token (with Bearer prefix) and client id to auth_token.json under "data" key.
            token_path = os.path.join(ANGELWEB_PATH, "auth_token.json")
            with open(token_path, "w") as file:
                json.dump({"data": {"auth_token": auth_token, "client_id": CLIENT_ID}}, file)
            logger.info(f"Auth token written to: {token_path}")
            
            logger.info("✅ Login Successful!")
            return smart_api, auth_token, refresh_token
        else:
            logger.error(f"❌ Login Failed: {response}")
            return None, None, None
    except Exception as e:
        logger.exception(f"Login error: {e}")
        return None, None, None

if __name__ == "__main__":
    smart_api, auth_token, refresh_token = login()
