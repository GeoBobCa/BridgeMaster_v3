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
    # Grab the first "word" that looks like a bid (Number + Letter)
    match = re.match(r"^([1-7](?:C|D|H|S|NT))", key.strip(), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None

def flatten_node(node, current_auction, gathered_rules, system_name):
    """
    Recursive function to walk the tree and build flat rules.
    """
    # 1. Process the current node (The Bid itself)
    if current_auction: # Skip the empty root
        last_bid = current_auction[-1]
        
        # Build the rule object
        rule = {
            "system": system_name, # Keeps the systems separated in the DB
            "auction": current_auction[:-1], # The context (everything before this bid)
            "bid": last_bid,
            "type": node.get("type", "Response"),
            "constraints": {
                "min_hcp": node.get("logic", {}).get("min_hcp", 0),
                "max_hcp": node.get("logic", {}).get("max_hcp", 37),
                "shape_requirements": node.get("logic", {}).get("shape"),
                "explanation": node.get("teaching", {}).get("nuance"), # Short explanation
                "nuance": node.get("teaching", {}).get("deep_dive"),   # The rich content
                "source": node.get("meta", {}).get("source")           # The Citation
            }
        }
        gathered_rules.append(rule)

    # 2. Process children (Responses)
    responses = node.get("responses", {})
    for key, child_node in responses.items():
        clean_key = clean_bid_key(key)
        
        if clean_key:
            # Recursion: Go deeper into the tree
            new_auction = current_auction + [clean_key]
            flatten_node(child_node, new_auction, gathered_rules, system_name)

def main():
    systems_dir = Path("systems")
    output_path = Path("systems/flat_rules.yaml")
    
    all_rules = []
    
    print("🌳 Flattening All System Trees...")

    # Find any file that looks like "*_tree.json"
    # This automatically picks up SAYC, Basic, and Standard
    for tree_file in systems_dir.glob("*_tree.json"):
        # Extract system name from filename (e.g. "sayc_tree.json" -> "sayc")
        system_name = tree_file.stem.replace("_tree", "")
        print(f"   Processing System: {system_name}...")
        
        try:
            with open(tree_file, "r", encoding="utf-8") as f:
                tree_data = json.load(f)
                
            # Walk the tree for this system
            for key, node in tree_data.items():
                clean_key = clean_bid_key(key)
                if clean_key:
                    flatten_node(node, [clean_key], all_rules, system_name)
            
            print(f"     -> Added rules from {tree_file.name}")
                    
        except Exception as e:
            print(f"   ❌ Error reading {tree_file.name}: {e}")

    # Configure Ruamel YAML for clean output
    yaml = YAML()
    yaml.default_flow_style = False  # Block style
    yaml.width = 4096                # Prevent line wrapping
    
    # Save Master Database
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(all_rules, f)
        
    print("-" * 30)
    print(f"✅ Database Updated! Contains {len(all_rules)} rules.")
    print(f"📄 Saved to: {output_path}")

if __name__ == "__main__":
    main()