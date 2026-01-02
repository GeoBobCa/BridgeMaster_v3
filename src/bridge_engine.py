from bridge_model import SUPPORTED_SYSTEMS

def check_hand_compliance(hand_stats, constraints):
    """
    Returns True if a hand matches the rule's requirements.
    """
    # 1. Check Points (Updated to use 'total_hcp' to match Bridge Model)
    # We use .get() with a fallback to support both 'hcp' (legacy) and 'total_hcp'
    points = hand_stats.get('total_hcp', hand_stats.get('hcp', 0))
    
    if points < constraints.get('min_hcp', 0): return False
    if points > constraints.get('max_hcp', 37): return False

    # 2. Check Shape
    req = constraints.get('shape_requirements', "").lower()
    if not req: return True

    suits = hand_stats['suits']
    
    # Majors
    if "spades" in req or "major" in req:
        min_len = 5 if "5+" in req else 4
        if suits['S']['count'] < min_len: return False
        
    if "hearts" in req or "major" in req:
        min_len = 5 if "5+" in req else 4
        if suits['H']['count'] < min_len: return False

    # Balanced
    if "balanced" in req:
        dist = [suits[s]['count'] for s in ['S','H','D','C']]
        if 0 in dist or 1 in dist: return False

    return True

def find_bid(hand_stats, rules, auction_history, target_system="SAYC_2/1_GF"):
    """
    Finds the correct bid using the System Filter.
    """
    # 1. Filter by Auction Path
    candidates = [r for r in rules if r.get('auction') == auction_history]
    
    # 2. Filter by System
    system_candidates = []
    for r in candidates:
        r_sys = r.get('system', 'ALL') 
        if r_sys == 'ALL' or r_sys == target_system:
            system_candidates.append(r)
            
    # 3. Check Compliance
    for rule in system_candidates:
        if check_hand_compliance(hand_stats, rule.get('constraints', {})):
            return rule
            
    return None