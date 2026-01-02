import os
from dotenv import load_dotenv

load_dotenv() # This loads the variables from .env

api_key = os.getenv("GOOGLE_API_KEY") # Replace with whatever name you used

if api_key is None:
    print("❌ ERROR: Python cannot find the API key. Check your .env path.")
elif api_key.startswith("AIza"):
    print(f"✅ SUCCESS: Key found! Starts with: {api_key[:8]}...")
else:
    print(f"⚠️ WARNING: Key found, but looks wrong: {api_key}")