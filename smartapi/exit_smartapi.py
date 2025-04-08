import os
import json
from dotenv import load_dotenv
from SmartApi import SmartConnect
from logzero import logger

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

def load_auth_data():
    """Load auth token and client ID from auth_token.json stored under a 'data' key."""
    token_path = os.path.join(ANGELWEB_PATH, "auth_token.json")
    if os.path.exists(token_path):
        with open(token_path, "r") as file:
            data = json.load(file)
            token_data = data.get("data", {})
            return token_data.get("auth_token"), token_data.get("client_id")
    return None, None

def attempt_logout(token, client_id, description, api_key):
    # Provide API key to SmartConnect so that X-PrivateKey header is set.
    smart_api = SmartConnect(api_key=api_key)
    smart_api.setAccessToken(token)
    response = smart_api.terminateSession(client_id)
    if response.get("status"):
        logger.info(f"Logout Successful with {description}! Response: {response}")
    else:
        logger.error(f"Logout Failed with {description}! Response: {response}")
    return response

def logout():
    try:
        # User selects the environment file to load.
        load_trading_env()
        api_key = os.getenv("API_KEY")
        if not api_key:
            logger.error("No API_KEY found in the environment. Ensure the .env file is set up correctly.")
            return
        
        auth_token, client_id = load_auth_data()
        if not auth_token or not client_id:
            logger.error("No valid auth token or client ID found. Please log in first.")
            return

        # Use only token without the Bearer prefix if present.
        if auth_token.startswith("Bearer "):
            auth_token = auth_token[len("Bearer "):]
        
        # Attempt logout with the token (without Bearer prefix).
        attempt_logout(auth_token, client_id, "token without Bearer prefix", api_key)
    
    except Exception as e:
        logger.exception(f"Logout error: {e}")

if __name__ == "__main__":
    logout()
