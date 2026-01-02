import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Check keys
g_key = os.getenv("GOOGLE_API_KEY")
gem_key = os.getenv("GEMINI_API_KEY")

print(f"🔑 GOOGLE_API_KEY found: {'Yes' if g_key else 'No'}")
print(f"🔑 GEMINI_API_KEY found: {'Yes' if gem_key else 'No'}")

# Pick one (Prioritize GEMINI_API_KEY if we are using that in the app)
key_to_use = gem_key if gem_key else g_key

print("\n📡 Connecting to Gemini...")
try:
    client = genai.Client(api_key=key_to_use)
    
    # Try the model we are using in the App
    print("   Sending request to 'gemini-2.0-flash'...")
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="Say 'Hello Bridge Player' if you can hear me."
    )
    print(f"\n✅ SUCCESS: {response.text}")
    
except Exception as e:
    print(f"\n❌ FAILURE: {e}")
    print("\n💡 TIP: If 'gemini-2.0-flash' failed, try changing the model in src/system_architect.py to 'gemini-1.5-flash'")