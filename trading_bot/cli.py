import sys
import typer
from typing import Optional
from bot.client import BinanceClient
from bot.orders import place_order
from bot.models import OrderRequest
from bot.display import display_health_check, display_order_summary, display_market_info, display_account_details, display_success, display_error
from bot.exceptions import BinanceError
from bot.validators import ValidationError

app = typer.Typer()

@app.command()
def check():
    """Health check command"""
    try:
        client = BinanceClient()
        ping = client.ping()
        balance = client.get_balance()
        display_health_check(ping, balance)
        display_success("Health check completed successfully")
    except Exception as e:
        display_error(f"Health check failed: {e}")

@app.command()
def account():
    """View futures account details"""
    try:
        client = BinanceClient()
        account_info = client.get_account_info()
        display_account_details(account_info)
        display_success("Account details retrieved successfully")
    except BinanceError as e:
        display_error(f"Binance error: {e}")
    except Exception as e:
        display_error(f"Unexpected error: {e}")

@app.command()
def place(
    symbol: str = typer.Option(..., help="Trading symbol, e.g., BTCUSDT"),
    side: str = typer.Option(..., help="Order side: BUY or SELL"),
    type: str = typer.Option(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, help="Order price (required for LIMIT orders)"),
):
    """Place an order"""
    try:
        request = OrderRequest(symbol=symbol, side=side, type=type, quantity=quantity, price=price)
        order = place_order(request)
        display_order_summary(order)
        display_success("Order placed successfully")
    except ValidationError as e:
        display_error(f"Validation error: {e}")
    except BinanceError as e:
        display_error(f"Binance error: {e}")
        if "margin" in str(e).lower() or "insufficient" in str(e).lower():
            try:
                client = BinanceClient()
                account_info = client.get_account_info()
                display_account_details(account_info)
            except BinanceError as nested:
                display_error(f"Unable to fetch account details: {nested}")
    except Exception as e:
        display_error(f"Unexpected error: {e}")

@app.command()
def info(symbol: str = typer.Option(..., help="Trading symbol, e.g., BTCUSDT")):
    """Get market information"""
    try:
        client = BinanceClient()
        price = client.get_price(symbol)
        display_market_info(symbol, price)
    except BinanceError as e:
        display_error(f"Binance error: {e}")
    except Exception as e:
        display_error(f"Unexpected error: {e}")


COMMON_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
VALID_SYMBOL_INFO = "Valid symbols must be uppercase and end with USDT."


def select_symbol() -> str:
    print("Choose a symbol:")
    for index, symbol in enumerate(COMMON_SYMBOLS, start=1):
        print(f"{index}) {symbol}")
    print(f"{len(COMMON_SYMBOLS) + 1}) Custom symbol")
    choice = input(f"Select symbol (1-{len(COMMON_SYMBOLS) + 1}): ").strip()
    if choice.isdigit():
        choice_int = int(choice)
        if 1 <= choice_int <= len(COMMON_SYMBOLS):
            return COMMON_SYMBOLS[choice_int - 1]
        if choice_int == len(COMMON_SYMBOLS) + 1:
            return input("Enter custom symbol (e.g. BTCUSDT): ").strip().upper()
    print("Invalid selection, defaulting to BTCUSDT.")
    return "BTCUSDT"


def select_side() -> str:
    print("Choose side:")
    print("1) BUY")
    print("2) SELL")
    choice = input("Select side (1-2): ").strip()
    if choice == "1":
        return "BUY"
    if choice == "2":
        return "SELL"
    print("Invalid selection, defaulting to BUY.")
    return "BUY"


def select_order_type() -> str:
    print("Choose order type:")
    print("1) MARKET")
    print("2) LIMIT")
    choice = input("Select order type (1-2): ").strip()
    if choice == "1":
        return "MARKET"
    if choice == "2":
        return "LIMIT"
    print("Invalid selection, defaulting to MARKET.")
    return "MARKET"


def interactive_menu() -> None:
    while True:
        print("\n=== Binance Futures CLI Bot ===")
        print("1) Health check")
        print("2) Market info")
        print("3) Place order")
        print("4) View account details")
        print("5) Exit")
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            check()
        elif choice == "2":
            print(VALID_SYMBOL_INFO)
            symbol = select_symbol()
            print("-" * 40)
            info(symbol)
        elif choice == "3":
            print(VALID_SYMBOL_INFO)
            try:
                client = BinanceClient()
                account_info = client.get_account_info()
                display_account_details(account_info)
            except BinanceError as e:
                display_error(f"Unable to fetch account details: {e}")

            symbol = select_symbol()
            print("-" * 40)
            side = select_side()
            order_type = select_order_type()
            quantity = float(input("Enter quantity: ").strip())
            price = None
            if order_type == "LIMIT":
                price = float(input("Enter price: ").strip())
            place(symbol=symbol, side=side, type=order_type, quantity=quantity, price=price)
        elif choice == "4":
            account()
        elif choice == "5":
            print("Exiting CLI bot.")
            break
        else:
            print("Invalid option. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            app()
        else:
            interactive_menu()
    except KeyboardInterrupt:
        display_error("Operation cancelled by user")
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        # Log full traceback internally
        import traceback
        from bot.logging_config import setup_logging
        logger = setup_logging()
        logger.critical(f"Unexpected error: {traceback.format_exc()}")