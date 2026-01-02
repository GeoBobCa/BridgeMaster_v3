import random
import json
import time
from pathlib import Path

# IMPORT OUR TESTED MODULES
from bridge_model import load_rules, HandData, SuitHolding, SUPPORTED_SYSTEMS
from bridge_engine import find_bid

# --- CONFIGURATION ---
TIMEOUT_SECONDS = 5
MAX_ATTEMPTS = 50000

class HandFactory:
    def __init__(self, rules_file_path):
        self.rules = load_rules(rules_file_path)
        
    def _deal_hand(self):
        """Creates a random bridge deal."""
        deck = list(range(52))
        random.shuffle(deck)
        hands = {
            "N": deck[0:13],
            "E": deck[13:26],
            "S": deck[26:39],
            "W": deck[39:52]
        }
        return hands

    def _analyze_hand(self, cards):
        """Calculates HCP and Distribution for a single hand."""
        # cards is a list of integers 0-51
        # 0=2C, 12=AC, 13=2D... 
        suits = {0: 'C', 1: 'D', 2: 'H', 3: 'S'}
        ranks = "23456789TJQKA"
        
        hand_data = {'S': [], 'H': [], 'D': [], 'C': []}
        hcp = 0
        
        for c in cards:
            suit_idx = c // 13
            rank_idx = c % 13
            suit_char = suits[suit_idx]
            rank_char = ranks[rank_idx]
            hand_data[suit_char].append(rank_idx)
            
            if rank_idx >= 9: # Jack or higher
                hcp += (rank_idx - 8) # J=1, Q=2, K=3, A=4

        # Format for our Data Model
        formatted_suits = {}
        dist_list = []
        
        for s in ['S', 'H', 'D', 'C']:
            ranks_indices = sorted(hand_data[s], reverse=True)
            cards_str = "".join([ranks[r] for r in ranks_indices])
            suit_hcp = sum([(r - 8) for r in ranks_indices if r >= 9])
            formatted_suits[s] = {
                "cards": cards_str,
                "hcp": suit_hcp,
                "count": len(ranks_indices)
            }
            dist_list.append(len(ranks_indices))

        dist_str = "=".join(map(str, dist_list))
        
        return {
            "total_hcp": hcp,
            "distribution": dist_str,
            "suits": formatted_suits
        }

    def generate_deal(self, target_auction, target_system="SAYC_2/1_GF"):
        """
        Deals hands until one matches the target auction sequence for the given system.
        """
        start_time = time.time()
        attempts = 0
        
        print(f"Factory started: Targeting {target_auction} using {target_system}...")

        while attempts < MAX_ATTEMPTS:
            attempts += 1
            if time.time() - start_time > TIMEOUT_SECONDS:
                return {"error": "Timeout", "attempts": attempts}

            # 1. Deal
            raw_hands = self._deal_hand()
            
            # 2. Analyze & Bid (Simulate the Table)
            # We assume Dealer is always Opener for simplicity in this version, 
            # or we rotate based on who is supposed to bid. 
            # For now, let's assume Dealer = North = Opener.
            
            # Helper to map auction turn to hand direction
            # Auction: ["1S"] -> Next is East. ["1S", "Pass"] -> Next is South.
            # 0:N, 1:E, 2:S, 3:W
            
            current_auction = []
            valid_deal = True
            explanations = []
            
            # Verify the sequence step-by-step
            # We only check the Target Auction. If the hands generate matches, we keep it.
            
            deal_record = {}
            
            # Pre-calculate stats for all 4 hands
            stats = {}
            for direction, cards in raw_hands.items():
                stats[direction] = self._analyze_hand(cards)

            # SIMULATION LOOP
            # We check if the hands naturally generate the target auction
            current_bidder_idx = 0 # Starts at North
            directions = ['N', 'E', 'S', 'W']
            
            for target_bid in target_auction:
                dir_char = directions[current_bidder_idx % 4]
                hand_stats = stats[dir_char]
                
                # Ask the Engine: What does this hand bid?
                rule = find_bid(hand_stats, self.rules, current_auction, target_system)
                
                bid_made = rule['bid'] if rule else "Pass"
                
                if bid_made != target_bid:
                    valid_deal = False
                    break # Failed match
                
                # Match found, advance state
                current_auction.append(bid_made)
                explanations.append(f"{dir_char} bids {bid_made}: {rule['constraints'].get('explanation', '')}")
                current_bidder_idx += 1

            if valid_deal:
                # SUCCESS!
                return {
                    "success": True,
                    "hands": stats,
                    "auction": current_auction,
                    "explanations": explanations,
                    "attempts": attempts
                }
        
        return {"error": "No match found", "attempts": attempts}

# --- CLI TEST ---
if __name__ == "__main__":
    # Test it independently
    rules_path = Path("systems/flat_rules.yaml")
    factory = HandFactory(rules_path)
    
    # Try to generate a standard 1NT opener
    result = factory.generate_deal(["1NT"], "AG_Basic")
    
    if result.get("success"):
        print(f"✅ Found a Deal in {result['attempts']} attempts!")
        print(f"North Hand: {result['hands']['N']['total_hcp']} HCP")
    else:
        print(f"❌ Failed: {result.get('error')}")