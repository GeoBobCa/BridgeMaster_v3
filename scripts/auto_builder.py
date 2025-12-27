# VERSION: 2.2 (Dec 28, 2025) - 2C Sequence Prompt
import os
import sys
import re
from google import genai
from add_node import add_node_to_tree 

# --- CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
client = genai.Client(api_key=API_KEY)

# --- SYSTEM PROMPT (Currently set for 2nd Negative) ---
SYSTEM_DEFINITION = """
### Audrey Grant Modern Standard
(Responder's Rebid: Fourth Suit Forcing)

Context: Auction 1D - 1H - 1S.
We have bid 3 suits. 
The unbid suit is CLUBS.

1. The Convention (Fourth Suit Forcing):
   - 2C: Artificial. Game Forcing. 
   - Meaning: "Partner, I have a game-forcing hand but no clear direction. Please describe your hand further (do you have a stopper in Clubs for NT?)."
   - Requirements: 12+ HCP.

2. Natural Bids:
   - 2D: Preference to Opener's first suit (Weak, 6-9).
   - 2H: Re-bidding own suit (6+ cards, Weak/Inviting).
   - 2NT: Natural, inviting (10-12), promises Club stopper.
"""

def generate_auction_logic(auction_key):
    print(f"🧠 Contacting Gemini ({MODEL_NAME})... asking for '{auction_key}' logic...")
    
    prompt = f"""
    ACT AS: Bridge System Architect.
    TASK: Generate the YAML nodes for the children of the auction: "{auction_key}".
    SYSTEM DEFINITION: {SYSTEM_DEFINITION}
    OUTPUT FORMAT: Provide ONLY valid YAML. No markdown. No parent key.
    """
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text

def clean_yaml_response(text):
    text = re.sub(r"```yaml", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/auto_builder.py \"AUCTION_KEY\"")
        sys.exit(1)

    auction_key = sys.argv[1]
    
    try:
        raw_yaml = generate_auction_logic(auction_key)
        cleaned_yaml = clean_yaml_response(raw_yaml)
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        sys.exit(1)
    
    print("\n--- GENERATED LOGIC ---")
    print(cleaned_yaml)
    print("-----------------------\n")

    if input(f"Save to '{auction_key}'? (y/n): ").strip().lower() == 'y':
        add_node_to_tree(auction_key, cleaned_yaml) 
    else:
        print("Discarded.")