# src/hand_generator.py (Fixed for N/S Bidding Only)
import random
import sys
from pathlib import Path

# --- PATH SETUP ---
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))
import bidding_engine 

# --- CONFIGURATION ---
PROJECT_ROOT = SCRIPT_DIR.parent 
SYSTEM_FILE = PROJECT_ROOT / "systems" / "flat_rules.yaml" 
OUTPUT_FILE = PROJECT_ROOT / "output" / "generated_hands.pbn"

TARGET_COUNT = 5
TARGET_START = ["1S", "2H"] 

SUITS = ['S', 'H', 'D', 'C']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
HCP_VALUES = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}

def deal_hands():
    deck = [r+s for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return [deck[0:13], deck[13:26], deck[26:39], deck[39:52]]

def analyze_hand(cards):
    stats = {"hcp": 0, "S": 0, "H": 0, "D": 0, "C": 0, "dummy_points": 0}
    for card in cards:
        rank, suit = card[:-1], card[-1]
        stats["hcp"] += HCP_VALUES.get(rank, 0)
        stats[suit] += 1
    
    shortness_pts = 0
    for s in SUITS:
        count = stats[s]
        if count == 0: shortness_pts += 5
        elif count == 1: shortness_pts += 3
        elif count == 2: shortness_pts += 1
    stats["dummy_points"] = stats["hcp"] + shortness_pts
    return stats

def format_pbn_hand(cards):
    holding = {'S': [], 'H': [], 'D': [], 'C': []}
    for card in cards:
        holding[card[-1]].append(card[:-1])
    order = "AKQJT98765432"
    pbn_str = ""
    for s in SUITS:
        suit_cards = sorted(holding[s], key=lambda x: order.index(x) if x in order else 99)
        pbn_str += "".join(suit_cards) + "."
    return pbn_str[:-1]

def get_explanation(rule):
    if not rule: return "Unknown"
    return rule.get('constraints', {}).get('explanation', 'Natural.')

# ==============================================================================
# MAIN SIMULATION LOOP
# ==============================================================================
def main():
    print(f"--- BRIDGE HAND FACTORY (N/S ONLY) ---")
    print(f"Loading Rules: {SYSTEM_FILE.name}")
    print(f"Target Start: {TARGET_START}")
    
    if not SYSTEM_FILE.exists():
        print(f"❌ Error: Cannot find config file.")
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    rules = bidding_engine.load_system(SYSTEM_FILE)
    
    hands_found = 0
    attempts = 0
    pbn_content = ""

    while hands_found < TARGET_COUNT:
        attempts += 1
        if attempts % 5000 == 0:
            print(f" ... dealt {attempts} hands. Found {hands_found} so far.")

        hands_list = deal_hands()
        
        auction_history = []     
        explanations = []        
        pass_count = 0           
        current_player_idx = 0   # 0=North, 1=East, 2=South, 3=West
        
        # --- THE BIDDING LOOP ---
        while True:
            current_hand = hands_list[current_player_idx]
            stats = analyze_hand(current_hand)
            
            # === LOGIC FIX: FORCE OPPONENTS TO PASS ===
            # If Player is East (1) or West (3), they MUST Pass.
            if current_player_idx in [1, 3]:
                bid = "Pass"
                explanation = "Opponent Pass"
                rule = None
            else:
                # Only N/S check the engine
                rule = bidding_engine.find_bid(stats, rules, auction_history)
                if rule:
                    bid = rule['bid']
                    explanation = get_explanation(rule)
                else:
                    bid = "Pass"
                    explanation = "System default."
            # ==========================================

            auction_history.append(bid)
            if bid != "Pass" and current_player_idx in [0, 2]:
                # Only record explanations for N/S
                explanations.append(f"{bid}: {explanation}")
            
            # Check Termination (3 Passes)
            if bid == "Pass": pass_count += 1
            else: pass_count = 0
            
            if len(auction_history) >= 4 and pass_count >= 3:
                break 
            
            current_player_idx = (current_player_idx + 1) % 4
            
            # Check deviation
            active_bids = [b for b in auction_history if b != "Pass"]
            if len(active_bids) <= len(TARGET_START):
                steps_taken = len(active_bids)
                if active_bids != TARGET_START[:steps_taken]:
                    break 

        # --- CHECK RESULT ---
        active_bids = [b for b in auction_history if b != "Pass"]
        
        if active_bids[:len(TARGET_START)] == TARGET_START:
            hands_found += 1
            print(f"✅ Match #{hands_found}: {active_bids}")
            
            pbn_deal = f"N:{format_pbn_hand(hands_list[0])} {format_pbn_hand(hands_list[1])} {format_pbn_hand(hands_list[2])} {format_pbn_hand(hands_list[3])}"
            expl_str = " | ".join(explanations)
            
            pbn_content += f'[Event "Generated Hand {hands_found}"]\n'
            pbn_content += f'[Site "BridgeMaster"]\n'
            pbn_content += f'[Deal "{pbn_deal}"]\n'
            pbn_content += f'[Dealer "N"]\n'
            pbn_content += f'[Note "{expl_str}"]\n'
            pbn_content += f'[Auction "N"]\n'
            pbn_content += " ".join(auction_history) + "\n\n"

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write(pbn_content)
    
    print(f"\nSaved {hands_found} hands to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()