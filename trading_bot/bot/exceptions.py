class BinanceError(Exception):
    pass

ERROR_MAP = {
    -2014: "Invalid API credentials.",
    -2015: "Invalid API key or insufficient permissions.",
    -2019: "Insufficient futures margin.",
    -1121: "Invalid trading symbol.",
    -1021: "System clock out of sync.",
    -1003: "Too many requests.",
    -1013: "Invalid quantity.",
    -1014: "Invalid price.",
}

def map_binance_error(code: int) -> str:
    return ERROR_MAP.get(code, f"Unknown Binance error: {code}")