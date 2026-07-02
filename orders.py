from bot.client import BinanceFuturesClient
from bot.validators import validate_inputs
from bot.logging_config import logger

def execute_bot_order(api_key: str, api_secret: str, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    # 1. Validate inputs
    valid_data = validate_inputs(symbol, side, order_type, quantity, price)
    
    # 2. Setup client
    client = BinanceFuturesClient(api_key, api_secret)
    
    # 3. Formulate Payload
    payload = {
        "symbol": valid_data["symbol"],
        "side": valid_data["side"],
        "type": valid_data["type"],
        "quantity": valid_data["quantity"]
    }
    
    if valid_data["type"] == "LIMIT":
        payload["price"] = valid_data["price"]
        payload["timeInForce"] = "GTC" # Good 'Til Cancelled (Required for Futures Limit)

    logger.info(f"--- Initating Order Request: {valid_data['side']} {valid_data['quantity']} {valid_data['symbol']} ({valid_data['type']}) ---")
    
    # 4. Fire Request
    return client.place_order(payload)