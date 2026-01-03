import json
import copy
from pathlib import Path

def simplify_node(node, bid_key):
    """
    Recursively walks the tree and deletes 'Advanced' branches.
    """
    # 1. Identify Complex Conventions to Prune
    # (Adjust this list based on what you consider "Too Advanced" for Basic)
    complex_conventions = [
        "2NT", # Jacoby 2NT (as a response to Major)
        "Splinter",
        "4C", "4D", # Splinters or Gerber on first round
        "3C", "3D", "3H", "3S" # Jump Shifts
    ]
    
    # 2. Prune Responses
    if "responses" in node:
        responses = node["responses"]
        keys_to_delete = []
        
        for key in list(responses.keys()):
            # Delete if it matches our "Complex" list
            if any(conv in key for conv in complex_conventions):
                # Exception: Keep 2NT if it's a natural opening (the root 2NT bid)
                if bid_key == "Root" and key == "2NT":
                    pass 
                # Exception: Keep 2NT if it is a standard response to 1NT (Inv)
                elif bid_key == "1NT" and key == "2NT":
                    pass
                else:
                    keys_to_delete.append(key)
            
            # Delete "4-Level Preemptive Raises" if you want Basic to be strictly 1-2-3
            # (Optional: Comment this out if Basic allows 1H-4H)
            # if "4" in key and ("H" in key or "S" in key): 
            #    keys_to_delete.append(key)

        for key in keys_to_delete:
            del responses[key]
            
        # Recursively simplify the children that survived
        for key, child in responses.items():
            simplify_node(child, key)

    # 3. Simplify Explanations (Optional Logic)
    # Example: Simplify "Semi-Forcing Dustbin" to "Weak Response"
    if "teaching" in node:
        if "Dustbin" in node["teaching"].get("nuance", ""):
             node["teaching"]["nuance"] = "Weak Response (6-9 HCP)."

def main():
    # Define Paths
    standard_path = Path("systems/audrey_grant_standard_tree.json")
    basic_path = Path("systems/audrey_grant_basic_tree.json")
    
    if not standard_path.exists():
        print(f"❌ Error: {standard_path} not found.")
        print("   -> Run 'python src/json_merger.py' first to build the Standard tree.")
        return

    print("✂️  Pruning Standard Tree to create Basic...")
    
    # Load Standard
    with open(standard_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create a Deep Copy (so we don't accidentally edit Standard)
    basic_data = copy.deepcopy(data)

    # Start Pruning
    for key, node in basic_data.items():
        simplify_node(node, key)
        
    # Save Basic
    with open(basic_path, "w", encoding="utf-8") as f:
        json.dump(basic_data, f, indent=2)
        
    print(f"✅ Created 'Audrey Grant Basic' at: {basic_path}")
    print("👉 Next: Run 'python src/tree_flattener.py' to add it to the database.")

if __name__ == "__main__":
    main()