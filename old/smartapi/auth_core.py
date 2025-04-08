import os
import pyotp
import json
from dotenv import load_dotenv
from SmartApi import SmartConnect
from logzero import logger

ANGELALGO_PATH = r"C:\Users\user\projects\angelalgo"

def load_trading_env():
    """Loads the .env.trading environment file."""
    env_file = ".env.trading"
    env_path = os.path.join(ANGELALGO_PATH, env_file)
    if load_dotenv(env_path):
        logger.info(f"✅ {env_file} loaded successfully!")
    else:
        logger.error(f"❌ Failed to load {env_file}!")
    return env_file
