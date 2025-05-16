from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Server is live!"

@app.route("/zerodha_callback")
def zerodha_callback():
    request_token = request.args.get('request_token')
    if request_token:
        print(f"✅ Request Token: {request_token}")
        return "✅ Request token received! Check Railway logs."
    else:
        return "❌ Request token not found."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
