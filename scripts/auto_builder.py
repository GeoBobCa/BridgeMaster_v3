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


## =============================================================
## ==========     START OF SYSTEM DEFINITION      ====================
## =============================================================


SYSTEM_DEFINITION = """
### Audrey Grant Modern Standard
(Responses to Minor Suit Openings: 1C / 1D)

Context: Partner opened 1C or 1D.

1. Major Suit Responses (Priority):
   - 1H: 6+ HCP, 4+ Hearts. (Show major first).
   - 1S: 6+ HCP, 4+ Spades. (Show major first).
   - Note: If holding both, bid the cheaper one (Hearts) or longer one.

2. No Trump (Balanced, No Major):
   - 1NT: 6-10 HCP, Balanced, No 4-card major.
   - 2NT: 11-12 HCP, Balanced, No 4-card major.
   - 3NT: 13-15 HCP, Balanced, No 4-card major.

3. Raises (Inverted Minors - Optional, but lets stick to simple for now):
   - 2C (over 1C): 6-10 HCP, 5+ Clubs. Simple Raise.
   - 3C (over 1C): 11-12 HCP, 5+ Clubs. Limit Raise.
   - 2D (over 1D): 6-10 HCP, 4+ Diamonds. Simple Raise.
   - 3D (over 1D): 11-12 HCP, 4+ Diamonds. Limit Raise.

4. New Minor (Forcing):
   - 1D (over 1C): 6+ HCP, 4+ Diamonds.
"""

## =============================================================
## ==========     END OF SYSTEM DEFINITION      ====================
## =============================================================

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