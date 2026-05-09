from decimal import Decimal, ROUND_DOWN
from typing import Optional

class ValidationError(Exception):
    pass

def validate_symbol(symbol: str) -> str:
    if not symbol.endswith("USDT"):
        raise ValidationError("Symbol must end with 'USDT'")
    if not symbol.isupper():
        raise ValidationError("Symbol must be uppercase")
    return symbol

def validate_side(side: str) -> str:
    if side not in ["BUY", "SELL"]:
        raise ValidationError("Side must be 'BUY' or 'SELL'")
    return side

def validate_type(order_type: str) -> str:
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError("Type must be 'MARKET' or 'LIMIT'")
    return order_type

def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than 0")
    # Round to 3 decimals
    return float(Decimal(str(quantity)).quantize(Decimal('0.001'), rounding=ROUND_DOWN))

def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValidationError("Price is required and must be greater than 0 for LIMIT orders")
        # Round to 2 decimals
        return float(Decimal(str(price)).quantize(Decimal('0.01'), rounding=ROUND_DOWN))
    return None

def validate_notional_value(quantity: float, price: Optional[float]) -> None:
    if price is None:
        return  # For MARKET orders, can't check notional
    notional = quantity * price
    if notional < 10:
        raise ValidationError("Notional value must be at least 10 USDT")

def validate_max_quantity(quantity: float) -> None:
    if quantity > 100:  # Arbitrary limit to prevent huge orders
        raise ValidationError("Quantity exceeds maximum allowed (100)")

def validate_order_request(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float]) -> None:
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_type(order_type)
    quantity = validate_quantity(quantity)
    price = validate_price(price, order_type)
    validate_notional_value(quantity, price)
    validate_max_quantity(quantity)