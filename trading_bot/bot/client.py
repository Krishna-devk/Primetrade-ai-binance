import time
import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .config import load_config
from .exceptions import BinanceError, map_binance_error
from .logging_config import setup_logging

logger = setup_logging()

class BinanceClient:
    def __init__(self):
        api_key, secret_key = load_config()
        self.client = Client(api_key, secret_key, testnet=True)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def ping(self) -> bool:
        try:
            self.client.futures_ping()
            logger.info("Binance connectivity check passed")
            return True
        except Exception as e:
            logger.error(f"Binance connectivity check failed: {e}")
            return False

    def get_balance(self) -> dict:
        try:
            balance = self.client.futures_account_balance()
            usdt_balance = next((b for b in balance if b['asset'] == 'USDT'), None)
            if usdt_balance:
                logger.info(f"USDT balance: {usdt_balance['balance']}")
                return usdt_balance
            else:
                raise BinanceError("USDT balance not found")
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Failed to get balance: {e}")
            raise BinanceError(map_binance_error(e.code)) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error getting balance: {e}")
            raise BinanceError("Network error") from e

    def get_price(self, symbol: str) -> float:
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Current price for {symbol}: {price}")
            return price
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Failed to get price for {symbol}: {e}")
            raise BinanceError(map_binance_error(e.code)) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error getting price: {e}")
            raise BinanceError("Network error") from e

    def get_account_info(self) -> dict:
        try:
            account_info = self.client.futures_account()
            logger.info("Fetched futures account information")
            return account_info
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Failed to get account info: {e}")
            raise BinanceError(map_binance_error(e.code)) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error getting account info: {e}")
            raise BinanceError("Network error") from e

    def create_order(self, symbol: str, side: str, type: str, quantity: str, price: str = None) -> dict:
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': type,
                'quantity': quantity,
                'timeInForce': 'GTC' if type == 'LIMIT' else None,
            }
            if price:
                params['price'] = price
            order = self.client.futures_create_order(**params)
            logger.info(f"Order placed: {side} {type} {symbol} qty={quantity} price={price}")
            return order
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Failed to create order: {e}")
            raise BinanceError(map_binance_error(e.code)) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error creating order: {e}")
            raise BinanceError("Network error") from e