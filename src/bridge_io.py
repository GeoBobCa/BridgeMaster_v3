import json
from pathlib import Path

# Constants for Analysis
HCP_VALUES = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
SUIT_ORDER = ['S', 'H', 'D', 'C']

def get_hand_stats(cards):
    """
    Takes a raw list of cards (e.g. ['SA', 'HK', ...]) and returns a 
    rich dictionary with HCP, counts, and formatted strings.
    """
    if not cards: return {}

    # 1. Parse and Sort
    holding = {'S': [], 'H': [], 'D': [], 'C': []}
    
    for card in cards:
        # Detect format (RankSuit vs SuitRank)
        if card[-1] in holding: 
            rank, suit = card[:-1], card[-1]
        else:
            suit, rank = card[0], card[1:]
        holding[suit].append(rank)

    order = "AKQJT98765432"
    
    # 2. Calculate Stats
    total_hcp = 0
    suit_details = {}
    distribution = []
    pbn_parts = []
    
    for suit in SUIT_ORDER:
        ranks = holding[suit]
        # Sort ranks
        sorted_ranks = sorted(ranks, key=lambda x: order.index(x) if x in order else 99)
        
        # Suit Stats
        suit_hcp = sum(HCP_VALUES.get(r, 0) for r in sorted_ranks)
        count = len(sorted_ranks)
        
        # Accumulate
        total_hcp += suit_hcp
        distribution.append(str(count))
        pbn_parts.append("".join(sorted_ranks))
        
        suit_details[suit] = {
            "cards": "".join(sorted_ranks),
            "hcp": suit_hcp,
            "count": count
        }

    # 3. Build Final Object
    return {
        "pbn_string": ".".join(pbn_parts), # "AK.QJ.T9.87"
        "total_hcp": total_hcp,
        "distribution": "=".join(distribution), # "2=2=2=7" (S=H=D=C)
        "suits": suit_details
    }

def save_deals_to_json(deals, filepath):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(deals, f, indent=2)

def load_deals_from_json(filepath):
    path = Path(filepath)
    if not path.exists(): return []
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def convert_generator_output(hands_map, auction, explanations, deal_id):
    """
    Standardizes the generator's raw data into our Rich JSON Object.
    """
    return {
        "id": deal_id,
        "format": "BridgeMaster_v2_Rich",
        "hands": {
            "N": get_hand_stats(hands_map["N"]),
            "E": get_hand_stats(hands_map["E"]),
            "S": get_hand_stats(hands_map["S"]),
            "W": get_hand_stats(hands_map["W"])
        },
        "auction": auction,
        "explanations": explanations
    }