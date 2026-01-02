"""
test_gemini_key.py

Usage:
    # Loads GEMINI_API_KEY from .env (if present), then env vars, then CLI arg
    python test_gemini_key.py
    
    # Or pass key directly (overrides .env)
    python test_gemini_key.py "your-key-here"
"""

import os
import sys
from pathlib import Path

try:
    # Try newer SDK first, fallback to older
    try:
        from google import genai
        SDK_MODULE = "google-genai"
    except ImportError:
        import google.generativeai as genai
        SDK_MODULE = "google-generativeai"
except ImportError:
    print("Error: Google AI SDK not installed.")
    print("Install with: pip install google-genai  # or: pip install google-generativeai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv not installed.")
    print("Install with: pip install python-dotenv")
    sys.exit(1)

TEST_MODEL = "gemini-2.0-flash"  # adjust if needed gemini-2.0-flash

def get_api_key() -> str:
    # Load .env file if present
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        print(f"✅ Loaded .env from {env_path}")
    
    # Prefer CLI arg, then env vars
    if len(sys.argv) > 1:
        key = sys.argv[1].strip()
        print("🔑 Using API key from command line")
        return key
    
    # Check common env var names
    for var_name in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        key = os.getenv(var_name)
        if key:
            print(f"🔑 Using API key from env var: {var_name}")
            return key.strip()
    
    print("❌ No API key found.")
    print("Expected GEMINI_API_KEY in:")
    print("  1. Command line: python test_gemini_key.py 'your-key'")
    print("  2. .env file: GEMINI_API_KEY=your-key-here")
    print("  3. Environment: export GEMINI_API_KEY=your-key-here")
    sys.exit(1)


def main():
    api_key = get_api_key()
    print(f"Using SDK: {SDK_MODULE}")
    print(f"Testing model: {TEST_MODEL}")
    print("-" * 50)

    try:
        # Create client (works for both SDK versions)
        if SDK_MODULE == "google-genai":
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=TEST_MODEL,
                contents="Say 'pong' if you can read this.",
            )
            text = getattr(response, "text", None)
        else:  # google-generativeai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(TEST_MODEL)
            response = model.generate_content("Say 'pong' if you can read this.")
            text = response.text if hasattr(response, 'text') else None

        print("✅ Gemini API key is ACTIVE!")
        if text:
            print(f"Model reply: {text[:200]}")
        print(f"Model: {TEST_MODEL}")
        
    except Exception as e:
        print("❌ Gemini API key test FAILED.")
        print(f"Error: {repr(e)}")
        print("\nCommon causes:")
        print("- Invalid/revoked key")
        print("- Key lacks access to this model")
        print("- Quota exceeded")
        print("- Network/proxy issues")
        sys.exit(1)


if __name__ == "__main__":
    main()
