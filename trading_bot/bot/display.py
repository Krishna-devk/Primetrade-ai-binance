from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .models import OrderResponse

console = Console()

def display_success(message: str):
    console.print(Panel.fit(f"[bold green]{message}[/bold green]", title="SUCCESS"))

def display_error(message: str):
    console.print(Panel.fit(f"[bold red]{message}[/bold red]", title="ERROR"))

def display_warning(message: str):
    console.print(Panel.fit(f"[bold yellow]{message}[/bold yellow]", title="WARNING"))

def display_info(message: str):
    console.print(Panel.fit(f"[cyan]{message}[/cyan]", title="INFO"))

def display_health_check(ping: bool, balance: dict):
    table = Table(title="Health Check")
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="green")
    table.add_row("Connectivity", "✓ PASS" if ping else "✗ FAIL")
    table.add_row("Balance", f"{balance['balance']} USDT")
    console.print(table)

def display_account_details(account_info: dict):
    table = Table(title="Futures Account Details")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    wallet_balance = account_info.get("totalWalletBalance", "N/A")
    margin_balance = account_info.get("totalMarginBalance", "N/A")
    unrealized = account_info.get("totalUnrealizedProfit", "N/A")
    available_balance = account_info.get("availableBalance", "N/A")
    table.add_row("Wallet Balance", str(wallet_balance))
    table.add_row("Margin Balance", str(margin_balance))
    table.add_row("Unrealized PnL", str(unrealized))
    table.add_row("Available Balance", str(available_balance))

    positions = account_info.get("positions", [])
    if positions:
        position_table = Table(title="Open Positions")
        position_table.add_column("Symbol", style="cyan")
        position_table.add_column("Position Side", style="white")
        position_table.add_column("Amount", style="white")
        position_table.add_column("Entry Price", style="white")
        position_table.add_column("Unrealized PnL", style="white")
        for position in positions:
            if float(position.get("positionAmt", 0)) != 0:
                position_table.add_row(
                    position.get("symbol", "N/A"),
                    position.get("positionSide", "N/A"),
                    position.get("positionAmt", "0"),
                    position.get("entryPrice", "0"),
                    position.get("unRealizedProfit", "0"),
                )
        console.print(position_table)

    console.print(table)

def display_order_summary(order: OrderResponse):
    table = Table(title="Order Summary")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Symbol", order.symbol)
    table.add_row("Order ID", str(order.order_id))
    table.add_row("Status", order.status)
    table.add_row("Side", order.side)
    table.add_row("Type", order.type)
    table.add_row("Quantity", str(order.quantity))
    if order.price:
        table.add_row("Price", str(order.price))
    table.add_row("Executed Qty", str(order.executed_qty))
    if order.avg_price:
        table.add_row("Avg Price", str(order.avg_price))
    console.print(table)
    if order.type == "LIMIT" and order.status == "NEW":
        display_info("This limit order remains open until market price reaches your specified value.")

def display_market_info(symbol: str, price: float):
    table = Table(title=f"Market Info for {symbol}")
    table.add_column("Symbol", style="cyan")
    table.add_column("Price", style="green")
    table.add_row(symbol, f"{price} USDT")
    console.print(table)