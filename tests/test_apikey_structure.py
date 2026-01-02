import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# repr() prints the raw string, revealing hidden \n or \r characters
print(f"DEBUG INFO: {repr(api_key)}")