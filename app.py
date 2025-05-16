from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import json

app = Flask(__name__)

# Zerodha credentials
api_key = "4ks47sd4y0turte2"
access_token_file = "access_token.txt"

# Load access token from file
with open(access_token_file, "r") as f:
    access_token = f.read().strip()

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

@app.route("/")
def home():
    return "Trading Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"Received webhook data: {data}")

    # Example TradingView alert format (customize as needed)
    # {
    #   "action": "buy",
    #   "symbol": "NSE:RELIANCE",
    #   "qty": 1
    # }

    action = data.get("action")
    symbol = data.get("symbol")
    qty = data.get("qty", 1)

    if not action or not symbol:
        return jsonify({"error": "Missing 'action' or 'symbol' in payload"}), 400

    try:
        # Place order
        if action.lower() == "buy":
            order_id = kite.place_order(
                variety=kite.VARIETY_REGULAR,
                exchange=kite.EXCHANGE_NSE,
                tradingsymbol=symbol.split(":")[1],  # Remove exchange prefix
                transaction_type=kite.TRANSACTION_TYPE_BUY,
                quantity=qty,
                product=kite.PRODUCT_MIS,
                order_type=kite.ORDER_TYPE_MARKET,
            )
        elif action.lower() == "sell":
            order_id = kite.place_order(
                variety=kite.VARIETY_REGULAR,
                exchange=kite.EXCHANGE_NSE,
                tradingsymbol=symbol.split(":")[1],
                transaction_type=kite.TRANSACTION_TYPE_SELL,
                quantity=qty,
                product=kite.PRODUCT_MIS,
                order_type=kite.ORDER_TYPE_MARKET,
            )
        else:
            return jsonify({"error": "Invalid action, must be 'buy' or 'sell'"}), 400

        print(f"Order placed successfully, order_id: {order_id}")
        return jsonify({"status": "success", "order_id": order_id})

    except Exception as e:
        print(f"Error placing order: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
