import jwt
import sys

token = sys.argv[1]
try:
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("Decoded token:", decoded)
except Exception as e:
    print(f"Error decoding token: {e}")
