def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    symbol = symbol.upper().strip()
    side = side.upper().strip()
    order_type = order_type.upper().strip()
    
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
        
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")
        
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order Type must be either 'MARKET' or 'LIMIT'.")
        
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
        
    if order_type == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")
        
    return {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "price": price if order_type == "LIMIT" else None
    }