from flask import Flask, request

app = Flask(__name__)

@app.route("/zerodha_callback")
def zerodha_callback():
    request_token = request.args.get('request_token')
    if request_token:
        print("Request Token received:", request_token)
        return "✅ Request token received! Check your terminal."
    else:
        return "❌ No request token received."

if __name__ == "__main__":
    app.run(port=5000)
