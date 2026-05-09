import os
from dotenv import load_dotenv

class ConfigError(Exception):
    pass

def load_config():
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    secret_key = os.getenv("BINANCE_SECRET_KEY")
    if not api_key or not secret_key:
        raise ConfigError("Missing Binance API credentials. Please set BINANCE_API_KEY and BINANCE_SECRET_KEY in .env file.")
    return api_key, secret_key