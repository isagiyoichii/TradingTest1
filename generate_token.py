import os
from kiteconnect import KiteConnect

api_key = "4ks47sd4y0turte2"
api_secret = "d4uapr67qe45vf98uwu8r1l01jood44c"

kite = KiteConnect(api_key=api_key)

# Get request_token from environment variable
request_token = os.getenv("REQUEST_TOKEN")

if not request_token:
    print("❌ Error: REQUEST_TOKEN env variable not set")
    exit(1)

try:
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    print("✅ Access Token:", access_token)

    # Optionally save to file
    with open("access_token.txt", "w") as f:
        f.write(access_token)
    print("✅ Access token saved to access_token.txt")

except Exception as e:
    print("❌ Error:", e)
