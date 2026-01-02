import random
import time
import sys
import logging
from pathlib import Path

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("FACTORY")

sys.path.append(str(Path(__file__).parent))
from bridge_model import load_rules, SUPPORTED_SYSTEMS
from bridge_engine import find_bid

TIMEOUT_SECONDS = 5
MAX_ATTEMPTS = 50000

class HandFactory:
    def __init__(self, rules_file_path):
        self.rules = load_rules(rules_file_path)
        logger.info(f"🏭 Factory initialized. Loaded {len(self.rules)} rules.")
        
    def _deal_hand(self):
        deck = list(range(52))
        random.shuffle(deck)
        return {"N": deck[0:13], "E": deck[13:26], "S": deck[26:39], "W": deck[39:52]}

    def _analyze_hand(self, cards):
        # ... (Same logic as before, abbreviated for brevity) ...
        suits = {0: 'C', 1: 'D', 2: 'H', 3: 'S'}
        ranks = "23456789TJQKA"
        hand_data = {'S': [], 'H': [], 'D': [], 'C': []}
        hcp = 0
        for c in cards:
            suit_idx = c // 13
            rank_idx = c % 13
            hand_data[suits[suit_idx]].append(rank_idx)
            if rank_idx >= 9: hcp += (rank_idx - 8)

        formatted_suits = {}
        dist_list = []
        for s in ['S', 'H', 'D', 'C']:
            ranks_indices = sorted(hand_data[s], reverse=True)
            cards_str = "".join([ranks[r] for r in ranks_indices])
            suit_hcp = sum([(r - 8) for r in ranks_indices if r >= 9])
            formatted_suits[s] = {"cards": cards_str, "hcp": suit_hcp, "count": len(ranks_indices)}
            dist_list.append(len(ranks_indices))
            
        return {"total_hcp": hcp, "distribution": "=".join(map(str, dist_list)), "suits": formatted_suits}

    def generate_deal(self, target_auction, target_system="SAYC_2/1_GF"):
        start_time = time.time()
        attempts = 0
        
        logger.info(f"Targeting: {target_auction} [{target_system}]")

        while attempts < MAX_ATTEMPTS:
            attempts += 1
            if time.time() - start_time > TIMEOUT_SECONDS:
                return {"error": "Timeout", "attempts": attempts}

            raw_hands = self._deal_hand()
            stats = {d: self._analyze_hand(c) for d, c in raw_hands.items()}
            
            current_auction = []
            valid_deal = True
            explanations = []
            
            # --- SIMULATION WITH DEBUGGING ---
            current_bidder_idx = 0 
            directions = ['N', 'E', 'S', 'W']
            
            for i, target_bid in enumerate(target_auction):
                dir_char = directions[current_bidder_idx % 4]
                hand_stats = stats[dir_char]
                
                rule = find_bid(hand_stats, self.rules, current_auction, target_system)
                bid_made = rule['bid'] if rule else "Pass"
                
                if bid_made != target_bid:
                    valid_deal = False
                    
                    # LOG REJECTION REASONS (Only for the first 5 attempts to avoid spam)
                    if attempts <= 5:
                        reason = "No Rule Found (Default Pass)" if not rule else f"Rule says {bid_made}"
                        logger.info(f"❌ Attempt {attempts} rejected at step {i+1} ({dir_char}). Wanted {target_bid}, got {bid_made}. Reason: {reason}")
                        if not rule:
                            logger.info(f"   Context was: {current_auction}")
                            logger.info(f"   Hand: {hand_stats['total_hcp']} HCP, {hand_stats['distribution']}")

                    break 
                
                current_auction.append(bid_made)
                if rule: explanations.append(f"{dir_char}: {rule['constraints'].get('explanation')}")
                current_bidder_idx += 1

            if valid_deal:
                logger.info(f"✅ MATCH FOUND in {attempts} attempts!")
                return {
                    "success": True,
                    "hands": stats,
                    "auction": current_auction,
                    "explanations": explanations,
                    "attempts": attempts
                }
        
        return {"error": "No match found", "attempts": attempts}