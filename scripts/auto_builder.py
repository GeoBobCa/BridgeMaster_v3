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
(Responses to 1 Spade)

Context: Partner opened 1S (shows 5+ Spades, 12-21 HCP).

1. Support Bids (We have 3+ Spades):
   - 2S: Simple Raise. 6-9 HCP, 3+ Spades.
   - 3S: Limit Raise. 10-12 HCP, 3+ Spades. Inviting.
   - 4S: Preemptive/Weak. 0-9 HCP, 5+ Spades (Law of Total Tricks).

2. Game Forcing Support (Conventions):
   - 2NT (Jacoby 2NT): 13+ HCP, 4+ Spades. Game Forcing. Asks for shortness.

3. No Trump (No Support):
   - 1NT: 6-12 HCP (Semi-Forcing). Denies 3 Spades.

4. New Suits (Natural):
   - 2C: 10+ HCP, 4+ Clubs. Forcing.
   - 2D: 10+ HCP, 4+ Diamonds. Forcing.
   - 2H: 10+ HCP, 5+ Hearts. Forcing. (Note: Requires 5 hearts normally at the 2-level).
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