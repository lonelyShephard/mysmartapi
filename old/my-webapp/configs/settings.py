import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    API_KEY = os.environ.get('API_KEY')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    PASSWORD = os.environ.get('PASSWORD')
    SMARTAPI_TOTP_SECRET = os.environ.get('SMARTAPI_TOTP_SECRET')
    ANGELALGO_PATH = r"C:\Users\user\projects\angelalgo"