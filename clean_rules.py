import sys
from pathlib import Path

# --- PATH FIX ---
# This tells Python: "Look in the 'src' folder for modules too"
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir / "src"))

# Now we can import correctly
from bridge_model import load_rules, save_rules

# TARGET TO PURGE
TARGET_AUCTION = ['1S'] 
TARGET_SYSTEM = "SAYC_2/1_GF"

def purge_section():
    # Use explicit path to be safe
    rules_path = current_dir / "systems" / "flat_rules.yaml"
    
    try:
        rules = load_rules(rules_path)
    except FileNotFoundError:
        print(f"❌ Could not find file at: {rules_path}")
        return

    initial_count = len(rules)
    
    # Keep rules that DO NOT match our target
    new_rules = [
        r for r in rules 
        if not (r.get('auction') == TARGET_AUCTION and r.get('system') == TARGET_SYSTEM)
    ]
    
    removed_count = initial_count - len(new_rules)
    
    
    if removed_count > 0:
        save_rules(rules_path, new_rules)
        print(f"✅ CLEANUP COMPLETE: Removed {removed_count} rules for {TARGET_AUCTION} in {TARGET_SYSTEM}.")
    else:
        print(f"ℹ️ Nothing to clean. No rules found for {TARGET_AUCTION} in {TARGET_SYSTEM}.")

if __name__ == "__main__":
    purge_section()