from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import json
import os

app = Flask(__name__)

# Zerodha credentials
api_key = "4ks47sd4y0turte2"
access_token_file = "access_token.txt"

# Load access token
if not os.path.exists(access_token_file):
    raise FileNotFoundError("Missing access_token.txt file")

with open(access_token_file, "r") as f:
    access_token = f.read().strip()

# Initialize Kite Connect
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

@app.route("/")
def home():
    return "✅ Trading Bot is Running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print(f"📩 Received webhook data: {data}")

        action = data.get("action", "").lower()
        symbol = data.get("symbol", "")
        qty = int(data.get("qty", 1))

        if not action or not symbol:
            return jsonify({"status": "error", "message": "Missing 'action' or 'symbol'"}), 400

        try:
            exchange, tradingsymbol = symbol.split(":")
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid symbol format. Use 'NSE:RELIANCE'"}), 400

        transaction_type = kite.TRANSACTION_TYPE_BUY if action == "buy" else (
            kite.TRANSACTION_TYPE_SELL if action == "sell" else None
        )

        if not transaction_type:
            return jsonify({"status": "error", "message": "Action must be 'buy' or 'sell'"}), 400

        # Place the order
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=transaction_type,
            quantity=qty,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET
        )

        print(f"✅ Order placed successfully. Order ID: {order_id}")
        return jsonify({"status": "success", "order_id": order_id})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
