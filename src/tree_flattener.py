import json
import re
import os
from pathlib import Path
from ruamel.yaml import YAML

def clean_bid_key(key):
    """
    Turns "2C (Stayman)" -> "2C"
    Turns "1H" -> "1H"
    """
    match = re.match(r"^([1-7](?:C|D|H|S|NT))", key.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None

def flatten_node(node, current_auction, gathered_rules, system_name):
    if current_auction: 
        last_bid = current_auction[-1]
        rule = {
            "system": system_name,
            "auction": current_auction[:-1],
            "bid": last_bid,
            "type": node.get("type", "Response"),
            "constraints": {
                "min_hcp": node.get("logic", {}).get("min_hcp", 0),
                "max_hcp": node.get("logic", {}).get("max_hcp", 37),
                "shape_requirements": node.get("logic", {}).get("shape"),
                "explanation": node.get("teaching", {}).get("nuance"),
                "nuance": node.get("teaching", {}).get("deep_dive"),
                "source": node.get("meta", {}).get("source")
            }
        }
        gathered_rules.append(rule)

    responses = node.get("responses", {})
    for key, child_node in responses.items():
        clean_key = clean_bid_key(key)
        if clean_key:
            new_auction = current_auction + [clean_key]
            flatten_node(child_node, new_auction, gathered_rules, system_name)

def main():
    tree_path = Path("systems/audrey_grant_standard_tree.json")
    output_path = Path("systems/flat_rules.yaml")
    
    if not tree_path.exists():
        print(f"❌ Error: {tree_path} not found.")
        return

    # --- NEW CHECK: Is the file empty? ---
    if os.path.getsize(tree_path) == 0:
        print(f"❌ Error: {tree_path} is empty (0 bytes).")
        print("   -> Open the file, paste the JSON content, and SAVE it.")
        return

    try:
        with open(tree_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: The file contains invalid data.")
        print(f"   -> {e}")
        return

    gathered_rules = []
    print("🌳 Walking the Decision Tree...")
    for key, node in tree_data.items():
        clean_key = clean_bid_key(key)
        if clean_key:
            flatten_node(node, [clean_key], gathered_rules, "audrey_grant_standard")
    
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.width = 4096 
    
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(gathered_rules, f)
        
    print(f"✅ Converted Tree into {len(gathered_rules)} Flat Rules!")
    print(f"📄 Saved to: {output_path}")

if __name__ == "__main__":
    main()