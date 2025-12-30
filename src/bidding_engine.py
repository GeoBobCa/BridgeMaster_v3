# src/bidding_engine.py (The "Flat" Version - Corrected)
from ruamel.yaml import YAML

def load_system(filepath):
    """Loads the flat list of rules using ruamel.yaml."""
    yaml = YAML(typ='safe', pure=True)
    with filepath.open("r", encoding="utf-8") as f:
        return yaml.load(f)

def check_constraints(hand, constraints):
    """(Checks HCP and Shape - No changes needed here)"""
    if not constraints: return True
    
    # 1. HCP Check
    hcp = hand.get('hcp', 0)
    if 'min_hcp' in constraints and hcp < constraints['min_hcp']: return False
    if 'max_hcp' in constraints and hcp > constraints['max_hcp']: return False
    
    # 2. Dummy Points Check
    d_pts = hand.get('dummy_points', 0)
    if 'min_dummy_points' in constraints and d_pts < constraints['min_dummy_points']: return False
    if 'max_dummy_points' in constraints and d_pts > constraints['max_dummy_points']: return False

    # 3. Shape Check
    req = constraints.get('shape_requirements')
    if req:
        suit_map = {"Spades": "S", "Hearts": "H", "Diamonds": "D", "Clubs": "C"}
        
        # Balanced
        if "Balanced" in req:
            counts = [hand['S'], hand['H'], hand['D'], hand['C']]
            if min(counts) < 2: return False
            if counts.count(2) > 1: return False

        for suit_name, key in suit_map.items():
            # "5+ Spades"
            if f"+ {suit_name}" in req:
                try:
                    needed = int(req.split(suit_name)[0].strip().split()[-1].replace("+", ""))
                    if hand[key] < needed: return False
                except: pass
            
            # "Max 1 Club"
            if f"Max 1 {suit_name[:-1]}" in req: 
                 if hand[key] > 1: return False
                 
    return True

def find_bid(hand, rules, current_auction_history):
    """
    Scans the rulebook for a rule that matches:
    1. The current auction history.
    2. The hand constraints.
    """
    for rule in rules:
        # A. Does the History Match?
        # We strip the "Pass" bids from history to match the YAML format
        # e.g. ["1S", "Pass", "2NT", "Pass"] becomes ["1S", "2NT"]
        active_bids = [b for b in current_auction_history if b != "Pass"]
        
        required_auction = rule.get('auction', [])
        
        # Ensure we are comparing lists
        if required_auction is None: required_auction = []
        
        if active_bids != required_auction:
            continue # This rule is for a different situation

        # B. Do the Constraints Match?
        if check_constraints(hand, rule.get('constraints')):
            return rule # Found it!
            
    return None