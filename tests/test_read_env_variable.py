import os
from dotenv import load_dotenv

# 1. Load the variables from .env
# By default, this looks for a .env file in the current directory
loaded = load_dotenv()

# Check if the file was found
if not loaded:
    print("⚠️  Warning: load_dotenv() did not find a .env file.")
else:
    print("✅ .env file loaded successfully.")

# 2. Try to access the specific variable
api_key = os.getenv("GEMINI_API_KEY")

# 3. Print the result
print("-" * 30)
if api_key:
    print(f"Success! The variable was read: {api_key}")
else:
    print("❌ Failed: The variable 'TEST_KEY' returned None.")
print("-" * 30)