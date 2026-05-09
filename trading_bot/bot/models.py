from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    side: str
    type: str
    quantity: float
    price: Optional[float] = None

@dataclass(frozen=True)
class OrderResponse:
    symbol: str
    order_id: int
    status: str
    side: str
    type: str
    quantity: float
    price: Optional[float] = None
    executed_qty: float = 0.0
    avg_price: Optional[float] = None