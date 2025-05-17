from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

# Load API key and access token from environment variables or fallback to defaults
api_key = os.getenv("API_KEY", "4ks47sd4y0turte2")  # Your API key here
api_secret = os.getenv("API_SECRET", "your_api_secret")  # Set this in Railway environment vars
access_token = os.getenv("ACCESS_TOKEN")

# If ACCESS_TOKEN not in env, try loading from file (for local dev)
if not access_token:
    try:
        with open("access_token.txt", "r") as f:
            access_token = f.read().strip()
        print("✅ Loaded access token from file")
    except FileNotFoundError:
        raise Exception("Access token not found! Set ACCESS_TOKEN env var or access_token.txt file.")

# Initialize KiteConnect and set access token
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

        if action == "buy":
            transaction_type = kite.TRANSACTION_TYPE_BUY
        elif action == "sell":
            transaction_type = kite.TRANSACTION_TYPE_SELL
        else:
            return jsonify({"status": "error", "message": "Action must be 'buy' or 'sell'"}), 400

        # Place the order
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=transaction_type,
            quantity=qty,
            product=kite.PRODUCT_MIS,
            order_type=kite.ORDER_TYPE_MARKET,
        )

        print(f"✅ Order placed successfully. Order ID: {order_id}")
        return jsonify({"status": "success", "order_id": order_id})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
