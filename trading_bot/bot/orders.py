import time
from .client import BinanceClient
from .models import OrderRequest, OrderResponse
from .validators import validate_order_request
from .logging_config import setup_logging

logger = setup_logging()

def place_order(request: OrderRequest) -> OrderResponse:
    validate_order_request(request.symbol, request.side, request.type, request.quantity, request.price)
    client = BinanceClient()
    start_time = time.time()
    quantity_str = str(request.quantity)
    price_str = str(request.price) if request.price else None
    order_data = client.create_order(request.symbol, request.side, request.type, quantity_str, price_str)
    execution_time = time.time() - start_time
    logger.info(f"Order executed in {execution_time:.2f}s")
    return OrderResponse(
        symbol=order_data['symbol'],
        order_id=order_data['orderId'],
        status=order_data['status'],
        side=order_data['side'],
        type=order_data['type'],
        quantity=float(order_data['origQty']),
        price=float(order_data.get('price', 0)) if order_data.get('price') else None,
        executed_qty=float(order_data.get('executedQty', 0)),
        avg_price=float(order_data.get('avgPrice', 0)) if order_data.get('avgPrice') else None,
    )