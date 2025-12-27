import sys
import os

# --- IMPORT FIX: Use ruamel.yaml instead of PyYAML ---
try:
    from ruamel.yaml import YAML
    yaml = YAML()
    yaml.preserve_quotes = True
except ImportError:
    print("CRITICAL ERROR: ruamel.yaml not found.")
    print("Please run: uv add ruamel.yaml")
    sys.exit(1)

# --- CONFIGURATION ---
# These paths assume you run the script from the BridgeMaster_v3 root folder
SYSTEM_DEF_PATH = "systems/audrey_grant_std.md"
TREE_FILE_PATH = "systems/bidding_tree.yaml"

def load_system_text():
    # Defensive check: Print current directory if file not found
    if not os.path.exists(SYSTEM_DEF_PATH):
        print(f"ERROR: Could not find system file at: {os.path.abspath(SYSTEM_DEF_PATH)}")
        print(f"Current working directory is: {os.getcwd()}")
        print("TIP: Make sure you are running this from the 'BridgeMaster_v3' root folder.")
        sys.exit(1)
        
    with open(SYSTEM_DEF_PATH, 'r') as f:
        return f.read()

def generate_prompt(auction_history: str, system_text: str):
    prompt = f"""
    ACT AS: Bridge System Architect (Audrey Grant Standard).
    
    CONTEXT:
    The current auction is: {auction_history}
    
    TASK:
    Generate the next valid bids for this specific auction state based strictly on the System Definition below.
    
    OUTPUT FORMAT:
    Produce ONLY valid YAML code representing a list of children nodes. Use this exact schema for each bid:
    
    - bid: "1S" (The bid string)
      type: "Response" (Opening, Response, Rebid, Competitive)
      convention: "Natural" (or Stayman, Jacoby, etc.)
      complexity: "Basic" (Basic, Intermediate, Advanced)
      forcing_status: "Forcing" (Forcing, Non-Forcing, Game-Forcing, Sign-off)
      inference: "What this bid tells partner (e.g., 6+ HCP, 4+ Spades)"
      explanation: "Teacher-style explanation of why this bid is chosen."
      hint_on_miss: "A hint if the student fails to find this bid."
      constraints:
        min_hcp: 6
        max_hcp: 21
        shape_requirements: "4+ Spades"
        evaluation_method: "Length Points" (or HCP, Dummy Points)
        
    SYSTEM DEFINITION:
    {system_text}
    """
    return prompt

def manual_input_loop(auction_path):
    system_text = load_system_text()
    
    print(f"\n--- BRIDGE MASTER v3: EXPANDING NODE '{auction_path}' ---")
    print("1. Copy the text below and paste it into Gemini.")
    print("-" * 60)
    print(generate_prompt(auction_path, system_text))
    print("-" * 60)
    print("2. Paste the YAML output from the LLM below. Type 'END' on a new line when finished.")
    print("--- PASTE YAML BELOW ---")
    
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    
    return "\n".join(lines)

def save_node_to_tree(auction_path, yaml_content):
    try:
        new_nodes = yaml.load(yaml_content)
        if not new_nodes:
            print("No data parsed.")
            return

        print(f"\n[QC CHECK] Reviewing {len(new_nodes)} new options for '{auction_path}':")
        for node in new_nodes:
            print(f" - Bid: {node.get('bid')} | {node.get('convention')}")
        
        confirm = input("\nDoes this look correct? (y/n): ")
        if confirm.lower() == 'y':
            with open(TREE_FILE_PATH, 'a') as f:
                f.write(f"\n# Children of {auction_path}\n")
                yaml.dump(new_nodes, f)
            print(f"Saved to {TREE_FILE_PATH}")
        else:
            print("Discarded.")

    except Exception as e:
        print(f"\nERROR: Invalid YAML. {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/expand_tree.py <auction_path>")
        sys.exit(1)
    
    auction = sys.argv[1]
    raw_yaml = manual_input_loop(auction)
    if raw_yaml:
        save_node_to_tree(auction, raw_yaml)