import sys
from ruamel.yaml import YAML
from pathlib import Path

# --- ROBUST PATH SETUP ---
# 1. Identify where this script is: .../BridgeMaster_v3/tests/
SCRIPT_DIR = Path(__file__).resolve().parent

# 2. Find the project root: .../BridgeMaster_v3/
PROJECT_ROOT = SCRIPT_DIR.parent

# 3. Construct path to the YAML file: .../BridgeMaster_v3/systems/bidding_tree.yaml
FILENAME = PROJECT_ROOT / "systems" / "bidding_tree.yaml"
# -------------------------

# Initialize the ruamel object
yaml = YAML(typ='safe')

if not FILENAME.exists():
    print(f"❌ Error: Could not find '{FILENAME}'")
    sys.exit(1)

try:
    with FILENAME.open("r", encoding="utf-8") as f:
        data = yaml.load(f)
        
        if isinstance(data, dict) and 'Dealer' in data:
            BIDDING_RULES = data['Dealer']
            print(f"✅ Successfully loaded rules from '{FILENAME}'")
        elif isinstance(data, list):
            BIDDING_RULES = data
        else:
            print("❌ Error: YAML structure unrecognized.")
            sys.exit(1)

except Exception as e:
    print(f"❌ Error reading YAML file: {e}")
    sys.exit(1)

# ==============================================================================
# 2. THE LOGIC
# ==============================================================================

def check_shape(hand, requirement):
    """
    Parses strings like "5+ Spades" or "Balanced" and checks the hand.
    """
    if requirement == "Balanced":
        counts = [hand['S'], hand['H'], hand['D'], hand['C']]
        # Definition: No singletons (min >= 2) and at most one doubleton
        return min(counts) >= 2 and counts.count(2) <= 1 

    if "+" in requirement:
        # Parse "5+ Spades"
        parts = requirement.split(" ")
        count_needed = int(parts[0].replace("+", ""))
        suit_name = parts[1]
        
        # Map full name to single letter key used in hand dict
        suit_map = {"Spades": "S", "Hearts": "H", "Diamonds": "D", "Clubs": "C"}
        key = suit_map.get(suit_name)
        
        if hand[key] >= count_needed:
            return True
            
    return False

def evaluate_hand(hand):
    """
    Iterates through the BIDDING_RULES top-to-bottom.
    Returns the FIRST bid that meets all constraints.
    """
    for rule in BIDDING_RULES:
        # Safety check: Ensure 'rule' is actually a dictionary
        if not isinstance(rule, dict):
            continue

        bid_name = rule.get('bid')
        constraints = rule.get('constraints')
        
        if not bid_name or not constraints:
            continue

        # 1. Check HCP
        hcp = hand['hcp']
        min_h = constraints.get('min_hcp', 0)
        max_h = constraints.get('max_hcp', 40)
        
        if not (min_h <= hcp <= max_h):
            continue 
            
        # 2. Check Shape (if required)
        shape_req = constraints.get('shape_requirements')
        if shape_req:
            if not check_shape(hand, shape_req):
                continue
        
        # If we get here, all constraints match!
        return bid_name

    return "No Bid Found"

# ==============================================================================
# 3. THE TEST DATA
# ==============================================================================

test_hands = [
    {
        "name": "Case A: Spade Trap (Majors vs Minors)",
        "hand": {"hcp": 13, "S": 5, "H": 3, "D": 4, "C": 1},
        "expected": "1S" 
    },
    {
        "name": "Case B: 5-5 Majors (Spades vs Hearts)",
        "hand": {"hcp": 13, "S": 5, "H": 5, "D": 2, "C": 1},
        "expected": "1S" 
    },
    {
        "name": "Case C: Better Minor (4D, 4C)",
        "hand": {"hcp": 13, "S": 2, "H": 3, "D": 4, "C": 4},
        "expected": "1D" 
    },
    {
        "name": "Case D: 1NT Check",
        "hand": {"hcp": 16, "S": 3, "H": 3, "D": 3, "C": 4},
        "expected": "1NT"
    }
]

# ==============================================================================
# 4. EXECUTION LOOP
# ==============================================================================

print("\n>>> BRIDGE BIDDING FILE TESTER <<<")

passed_count = 0

for case in test_hands:
    result = evaluate_hand(case['hand'])
    
    is_correct = (result == case['expected'])
    status = "✅ PASS" if is_correct else f"❌ FAIL (Expected {case['expected']})"
    
    print(f"Test: {case['name']:<40} Result: {result}  [{status}]")
    
    if is_correct:
        passed_count += 1

print("-" * 60)
print(f"SUMMARY: {passed_count}/{len(test_hands)} Tests Passed")
print("-" * 60)