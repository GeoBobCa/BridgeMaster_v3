import sys
from ruamel.yaml import YAML
from pathlib import Path

# ==============================================================================
# 1. CONFIGURATION
# ==============================================================================


# --- ROBUST PATH SETUP ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
FILENAME = PROJECT_ROOT / "systems" / "bidding_tree.yaml"
# -------------------------

# ==============================================================================
# 2. THE ENGINE
# ==============================================================================

def check_constraints(hand, constraints):
    """
    Evaluates a hand against a set of constraints (HCP, Shape, Points).
    """
    # 1. Check HCP
    hcp = hand.get('hcp', 0)
    min_h = constraints.get('min_hcp', 0)
    max_h = constraints.get('max_hcp', 40)
    if not (min_h <= hcp <= max_h):
        return False

    # 2. Check Dummy Points (if applicable)
    if 'min_dummy_points' in constraints:
        dp = hand.get('dummy_points', hcp) # Fallback to HCP if DP not calculated
        if dp < constraints['min_dummy_points']:
            return False
        if 'max_dummy_points' in constraints:
            if dp > constraints['max_dummy_points']:
                return False

    # 3. Check Shape Requirements (Parsing strings like "5+ Spades")
    req = constraints.get('shape_requirements')
    if req:
        # Simple parser for "5+ Suit"
        # In a real app, this would be a more robust regex or logic class
        suit_map = {"Spades": "S", "Hearts": "H", "Diamonds": "D", "Clubs": "C"}
        
        if "Balanced" in req:
            # Simplified balanced check: No singleton
            counts = [hand['S'], hand['H'], hand['D'], hand['C']]
            if min(counts) < 2: return False

        for suit_name, key in suit_map.items():
            if f"+ {suit_name}" in req: # e.g. "5+ Spades"
                # Extract number before the suit name
                try:
                    parts = req.split(suit_name)[0].strip().split()
                    needed = int(parts[-1].replace("+", ""))
                    if hand[key] < needed: return False
                except:
                    pass # parsing error fallback
    
    return True

def find_bid(hand, bid_list, current_system="Grant_Standard"):
    """
    Searches a list of bids for the first match that satisfies:
    1. The System Tag (or 'All')
    2. The Constraints
    """
    if not bid_list:
        return None

    for rule in bid_list:
        # --- A. SYSTEM CHECK ---
        allowed_systems = rule.get('systems', ["All"])
        if "All" not in allowed_systems and current_system not in allowed_systems:
            continue # Skip this bid, it's not for our system

        # --- B. CONSTRAINT CHECK ---
        constraints = rule.get('constraints', {})
        if check_constraints(hand, constraints):
            return rule # Return the whole rule object (so we can see children)

    return None

def run_simulation(dealer_hand, responder_hand, system_mode):
    """
    Simulates one round of bidding: Dealer Open -> Responder Reply
    """
    print(f"\n--- Simulation: {system_mode} ---")
    
    # Load YAML
    yaml = YAML(typ='safe')
    with open(FILENAME, "r") as f:
        data = yaml.load(f)
        root_bids = data['Dealer']

    # 1. DEALER BIDS
    opening_rule = find_bid(dealer_hand, root_bids, system_mode)
    
    if not opening_rule:
        print("Dealer: Pass (No opening found)")
        return

    opening_bid_name = opening_rule['bid']
    print(f"Dealer:   {opening_bid_name}  ({opening_rule['convention']})")

    # 2. RESPONDER BIDS
    # Look for the 'Responder' block nested inside the opening rule
    responder_options = opening_rule.get('Responder')
    
    if not responder_options:
        print("Responder: (No response logic defined for this opening)")
        return

    response_rule = find_bid(responder_hand, responder_options, system_mode)
    
    if response_rule:
        print(f"Responder: {response_rule['bid']}  ({response_rule['convention']})")
    else:
        print("Responder: Pass (No fitting response found)")

# ==============================================================================
# 3. TEST SCENARIOS
# ==============================================================================

# Hand A: Solid Opening Hand
dealer_hand = {
    "hcp": 13, 
    "S": 5, "H": 3, "D": 3, "C": 2
}

# Hand B: 13 Points, 4 Spades (The "Jacoby 2NT" Test)
# In Basic: This is a natural Limit Raise (too strong for 2NT? or limits to 12?)
# In Standard: This is Jacoby 2NT (Game Force)
responder_hand = {
    "hcp": 13, "dummy_points": 14,
    "S": 4, "H": 3, "D": 3, "C": 3
}

if __name__ == "__main__":

    if not FILENAME.exists():
        print(f"Error: Could not find {FILENAME}")
    else:
        # TEST 1: Run in "Grant_Basic" mode
        # Expected: Dealer 1S -> Responder 4S (Game Raise) 
        # (Because 2NT in Basic is limited to 12 HCP, so with 13 HCP logic falls through to 4S)
        run_simulation(dealer_hand, responder_hand, system_mode="Grant_Basic")

        # TEST 2: Run in "Grant_Standard" mode
        # Expected: Dealer 1S -> Responder 2NT (Jacoby 2NT)
        run_simulation(dealer_hand, responder_hand, system_mode="Grant_Standard")