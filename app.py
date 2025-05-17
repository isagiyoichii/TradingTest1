from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

# Load API key and secret from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

if not api_key or not api_secret:
    raise Exception("API_KEY and API_SECRET must be set as environment variables")

access_token_file = "access_token.txt"
access_token = None

# Initialize KiteConnect with API key only for now
kite = KiteConnect(api_key=api_key)

# Try to load access token from file and set it
def load_access_token():
    global access_token
    if os.path.exists(access_token_file):
        with open(access_token_file, "r") as f:
            access_token = f.read().strip()
            kite.set_access_token(access_token)
            print("✅ Loaded access token from file")
    else:
        print("⚠️ access_token.txt file not found, login required")

load_access_token()

@app.route("/")
def home():
    return "✅ Trading Bot is Running!"

@app.route("/login_url")
def login_url():
    # Returns the login URL to get the request_token manually
    url = kite.login_url()
    return jsonify({"login_url": url})

@app.route("/generate_token", methods=["POST"])
def generate_token():
    global access_token
    data = request.json
    request_token = data.get("request_token")

    if not request_token:
        return jsonify({"error": "Missing request_token"}), 400

    try:
        session_data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = session_data["access_token"]

        # Save access token to file
        with open(access_token_file, "w") as f:
            f.write(access_token)

        # Update kite instance with new access token
        kite.set_access_token(access_token)

        print("✅ Access token generated and saved")
        return jsonify({"access_token": access_token})

    except Exception as e:
        print(f"❌ Error generating access token: {e}")
        return jsonify({"error": str(e)}), 500

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
