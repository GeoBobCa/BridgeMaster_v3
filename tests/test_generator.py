import sys
from pathlib import Path

# --- SETUP PATHS ---
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.append(str(src_dir))

import hand_generator 
import bidding_engine

# --- DIAGNOSTICS ---
print("--- 🔍 GENERATOR PROBE ---")

# 1. Check Paths
print(f"1. Checking Paths...")
rules_path = src_dir.parent / "systems" / "flat_rules.yaml"
print(f"   Looking for rules at: {rules_path}")

if not rules_path.exists():
    print("   ❌ FATAL: Rules file NOT found!")
    sys.exit(1)
else:
    print("   ✅ Rules file exists.")

# 2. Check Rule Loading
print("\n2. Loading Rules...")
try:
    rules = bidding_engine.load_system(rules_path)
    print(f"   ✅ Loaded {len(rules)} rules.")
except Exception as e:
    print(f"   ❌ FATAL: Rule loading crashed: {e}")
    sys.exit(1)

# 3. Simulate One Deal
print("\n3. Simulating a Deal...")
# Override config manually
hand_generator.SYSTEM_FILE = rules_path
hand_generator.TARGET_START = ["1S", "2D"] 
hand_generator.TARGET_COUNT = 1

try:
    print(f"   Target: {hand_generator.TARGET_START}")
    
    # Manually run the internal logic loop for 1 attempt
    hands_map = hand_generator.deal_hands()
    print("   ✅ Hands dealt.")
    
    # Check North's stats
    n_stats = hand_generator.analyze_hand(hands_map["N"])
    print(f"   North Stats: {n_stats['hcp']} HCP")
    
    # Try to find a bid
    bid_rule = bidding_engine.find_bid(n_stats, rules, [])
    if bid_rule:
        print(f"   North would bid: {bid_rule['bid']}")
    else:
        print(f"   North would bid: Pass (No rule found)")
    
    print("\n✅ PROBE COMPLETE: The components are working.")
    print("If you see this, the issue is likely in how Streamlit calls the generator.")

except Exception as e:
    print(f"   ❌ CRASH IN GENERATOR LOGIC: {e}")