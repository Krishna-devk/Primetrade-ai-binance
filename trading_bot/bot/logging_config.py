import logging
import os
from datetime import datetime

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger