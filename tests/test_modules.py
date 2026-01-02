print("--- STARTING TEST ---")
import sys
from pathlib import Path

# 1. SETUP PATHS
current_dir = Path(__file__).resolve().parent
src_path = current_dir.parent / "src"
sys.path.append(str(src_path))

try:
    # 2. IMPORT MODULES
    from bridge_engine import find_bid
    print("✅ Imported bridge_engine successfully")
except ImportError as e:
    print(f"❌ Failed to import bridge_engine: {e}")
    sys.exit(1)

# 3. SETUP TEST DATA
mock_rules = [
    {
        "auction": [], 
        "bid": "1NT_AG", 
        "system": "AG_Basic", 
        "constraints": {"min_hcp": 16, "max_hcp": 18, "shape_requirements": "Balanced"}
    },
    {
        "auction": [], 
        "bid": "1NT_SAYC", 
        "system": "SAYC_2/1_GF", 
        "constraints": {"min_hcp": 15, "max_hcp": 17, "shape_requirements": "Balanced"}
    }
]

# A hand with 15 Points (Matches SAYC, Fails AG)
hand_15 = {
    "total_hcp": 15,
    "suits": {
        "S": {"count": 3}, 
        "H": {"count": 4}, 
        "D": {"count": 3}, 
        "C": {"count": 3}
    }
}

print("\n--- RUNNING SCENARIOS ---")

# TEST 1: Ask for Audrey Grant Basic
result_ag = find_bid(hand_15, mock_rules, [], "AG_Basic")
bid_ag = result_ag['bid'] if result_ag else "Pass"
print(f"1. System: AG_Basic    | Hand: 15 HCP | Result: {bid_ag}")

# TEST 2: Ask for SAYC 2/1
result_sayc = find_bid(hand_15, mock_rules, [], "SAYC_2/1_GF")
bid_sayc = result_sayc['bid'] if result_sayc else "Pass"
print(f"2. System: SAYC_2/1  | Hand: 15 HCP | Result: {bid_sayc}")

# 4. VERDICT
print("-" * 30)
if bid_ag == "Pass" and bid_sayc == "1NT_SAYC":
    print("✅ SUCCESS: The logic engine correctly separated the systems!")
else:
    print("❌ FAILURE: Logic error. Please check bridge_engine.py")