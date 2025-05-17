from flask import Flask, request
from kiteconnect import KiteConnect
import os

app = Flask(__name__)

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
kite = KiteConnect(api_key=api_key)

@app.route("/")
def home():
    return "✅ Token Generator is Live. Visit /login to get request_token."

@app.route("/login")
def login():
    return f"🔗 Click to login: <a href='{kite.login_url()}' target='_blank'>{kite.login_url()}</a>"

@app.route("/access", methods=["GET"])
def get_access_token():
    request_token = request.args.get("request_token")
    if not request_token:
        return "❌ Missing request_token in query params", 400

    try:
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        with open("access_token.txt", "w") as f:
            f.write(access_token)
        return f"✅ Access token saved: {access_token}"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
