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
(Responses to 1NT Opening)

Context: Partner opened 1NT (15-17 HCP, Balanced).

1. Stayman Convention (2C):
   - 2C (Var A): 8+ HCP, 4+ Hearts. (Ask for major).
   - 2C (Var B): 8+ HCP, 4+ Spades. (Ask for major).
   *Note: We list this twice so either suit triggers the bid.*

2. Jacoby Transfers (Announce 5+ card majors):
   - 2D: Transfer to Hearts. 0+ HCP, 5+ Hearts. (Partner must bid 2H).
   - 2H: Transfer to Spades. 0+ HCP, 5+ Spades. (Partner must bid 2S).

3. Natural / Invitations (No Major Fit):
   - 2NT: Invitational. 8-9 HCP, Balanced. (Invites 3NT).
   - 3NT: Game Sign-off. 10-15 HCP, Balanced.
   - Pass: Weak. 0-7 HCP.

Priority:
1. Check for 5-card Majors (Transfers) FIRST.
2. Then check for 4-card Majors (Stayman).
3. Then bid NT naturally.
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