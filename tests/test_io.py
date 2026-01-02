import sys
from pathlib import Path

# --- SETUP PATHS ---
# Add the 'src' folder to Python's path so we can import bridge_io
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.append(str(src_dir))

import bridge_io

# --- TEST DATA ---
# This simulates what the Generator creates internally
dummy_hands_map = {
    "N": ["SA", "SK", "SQ", "H2", "H3", "H4", "D5", "D6", "C7", "C8", "C9", "CT", "CJ"],
    "E": ["S2", "S3", "S4", "HA", "HK", "HQ", "D7", "D8", "CA", "CK", "CQ", "C2", "C3"],
    "S": ["S5", "S6", "S7", "H5", "H6", "H7", "DA", "DK", "DQ", "C4", "C5", "C6", "DJ"],
    "W": ["S8", "S9", "ST", "H8", "H9", "HT", "D2", "D3", "D4", "D9", "DT", "HJ", "SJ"]
}

dummy_auction = ["1S", "Pass", "2D", "Pass"]
dummy_explanations = ["1S: Opening", "Pass: ...", "2D: Response", "Pass: ..."]

# --- RUN TESTS ---
print("1. Testing Hand Analysis (get_hand_stats)...")
# Test North's hand
north_stats = bridge_io.get_hand_stats(dummy_hands_map["N"])
print(f"   North PBN:  {north_stats['pbn_string']}")
print(f"   North HCP:  {north_stats['total_hcp']}")
print(f"   North Dist: {north_stats['distribution']}")
print(f"   Suits Detail: {north_stats['suits']}")

print("\n2. Testing Formatting (convert_generator_output)...")
formatted_deal = bridge_io.convert_generator_output(
    dummy_hands_map, dummy_auction, dummy_explanations, 99
)
print("   Object Created Successfully.")

print("\n3. Testing Save/Load (JSON)...")
test_file = current_dir / "test_output.json"
try:
    # SAVE
    bridge_io.save_deals_to_json([formatted_deal], test_file)
    print(f"   Saved to {test_file}")
    
    # LOAD
    loaded_data = bridge_io.load_deals_from_json(test_file)
    print(f"   Loaded back {len(loaded_data)} deal(s).")
    
    # VERIFY
    loaded_pbn = loaded_data[0]['hands']['N']['pbn_string']
    if loaded_pbn == north_stats['pbn_string']:
        print("   ✅ SUCCESS: Data integrity verified.")
    else:
        print("   ❌ FAILURE: Data mismatch.")

except Exception as e:
    print(f"   ❌ CRASH: {e}")