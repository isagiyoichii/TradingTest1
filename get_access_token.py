from kiteconnect import KiteConnect

# Your Zerodha API credentials
api_key = "4ks47sd4y0turte2"
api_secret = "d4uapr67qe45vf98uwu8r1l01jood44c"

# Replace this with the request token you got from Railway logs
request_token = "7ael6wuZOsRwj6DUVnssoZki7WzAeN9a"

kite = KiteConnect(api_key=api_key)

try:
    # Generate session (access token)
    data = kite.generate_session(request_token=request_token, api_secret=api_secret)
    access_token = data["access_token"]
    
    print(f"✅ Access Token: {access_token}")

    # Save the access token to a file for future use
    with open("access_token.txt", "w") as f:
        f.write(access_token)

except Exception as e:
    print(f"❌ Error while generating access token: {e}")
