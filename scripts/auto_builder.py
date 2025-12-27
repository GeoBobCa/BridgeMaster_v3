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
(Responses to 1 Heart)

Context: Partner opened 1H (shows 5+ Hearts, 12-21 HCP).

1. Support Bids (We have 3+ Hearts):
   - 2H: Simple Raise. 6-9 HCP, 3+ Hearts.
   - 3H: Limit Raise. 10-12 HCP, 3+ Hearts. Inviting.
   - 4H: Preemptive/Weak. 0-9 HCP, 5+ Hearts (Law of Total Tricks).

2. Game Forcing Support (Conventions):
   - 2NT (Jacoby 2NT): 13+ HCP, 4+ Hearts. Game Forcing. Asks for shortness.
   - 3S/4C/4D (Splinters): Double Jump Shift. Shows 4+ Hearts, Game Forcing (13+), and a singleton/void in the bid suit.

3. No Trump (No Support):
   - 1NT: 6-12 HCP (Semi-Forcing). Denies 3 Hearts. Denies 4 Spades.

4. New Suits (Natural):
   - 1S: 4+ Spades, 6+ HCP. Forcing 1 Round.
   - 2C/2D: 4+ card suit, 10+ HCP. Forcing 1 Round.
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