import argparse
import os
import sys
from bot.orders import execute_bot_order

def main():
    parser = argparse.ArgumentParser(description="Primetrade.ai Simplified Binance Futures Testnet Trading Bot")
    
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order direction")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order execution type")
    parser.add_argument("--quantity", required=True, type=float, help="Asset amount to trade")
    parser.add_argument("--price", type=float, help="Price (Mandatory if order type is LIMIT)")

    args = parser.parse_args()

    # Fetch Credentials securely from Environment Variables
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")

    if not api_key or not api_secret:
        print("\n[ERROR] Missing Credentials! Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET environment variables.\n")
        sys.exit(1)

    print("\n================ ORDER REQUEST SUMMARY ================")
    print(f"Symbol:   {args.symbol.upper()}")
    print(f"Side:     {args.side.upper()}")
    print(f"Type:     {args.type.upper()}")
    print(f"Quantity: {args.quantity}")
    if args.type.upper() == "LIMIT":
        print(f"Price:    {args.price}")
    print("========================================================\n")

    try:
        response = execute_bot_order(
            api_key=api_key,
            api_secret=api_secret,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
        
        print("✔ ORDER SUCCESSFUL")
        print(f"Order ID:     {response.get('orderId')}")
        print(f"Status:       {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        print(f"Avg Price:    {response.get('avgPrice', 'N/A')}\n")

    except Exception as e:
        print(f"✘ ORDER FAILED: {str(e)}\n")

if __name__ == "__main__":
    main()