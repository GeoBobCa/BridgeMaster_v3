# VERSION: 3.1 (Dec 28, 2025) - Object Model + Smart Keys + Quality Points
import os
import re
from ruamel.yaml import YAML

class BidResult:
    """
    A simple container for the Engine's decision.
    Carries the Bid string, the Explanation, and any Teaching Alerts.
    """
    def __init__(self, bid, explanation=None, alert=None):
        self.bid = bid
        self.explanation = explanation  # From the YAML
        self.alert = alert              # Runtime warnings (e.g. "Hand Upgraded")

    def __str__(self):
        return self.bid

class BridgeHand:
    def __init__(self, spades_str, hearts_str, diamonds_str, clubs_str):
        self.suits = {
            'S': self._parse_suit(spades_str),
            'H': self._parse_suit(hearts_str),
            'D': self._parse_suit(diamonds_str),
            'C': self._parse_suit(clubs_str)
        }
        self.hcp = self._calculate_hcp()
        self.quality_hcp = self._calculate_quality()
        self.distribution = {s: len(cards) for s, cards in self.suits.items()}
        self.is_balanced = self._check_balanced()

    def _parse_suit(self, card_str):
        return list(card_str.replace(" ", "").upper())

    def _calculate_hcp(self):
        values = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
        total = 0
        for suit in self.suits.values():
            for card in suit:
                if card in values: total += values[card]
        return total

    def _calculate_quality(self):
        # Statistical Scale: A=4.5, K=3.0, Q=1.5, J=0.75, T=0.25
        values = {'A': 4.5, 'K': 3.0, 'Q': 1.5, 'J': 0.75, 'T': 0.25}
        total = 0.0
        for suit in self.suits.values():
            for card in suit:
                if card in values: total += values[card]
                elif card == '1' and '0' in suit: total += 0.25
        return total

    def _check_balanced(self):
        counts = sorted(self.distribution.values())
        return counts in [[3,3,3,4], [2,3,4,4], [2,3,3,5]]

    def length_of(self, suit_char):
        return self.distribution.get(suit_char, 0)

class BiddingEngine:
    def __init__(self, system_file_path):
        self.yaml = YAML()
        if not os.path.exists(system_file_path):
            raise FileNotFoundError(f"System file missing: {system_file_path}")
        
        with open(system_file_path, 'r', encoding='utf-8') as f:
            self.system = self.yaml.load(f)

    def find_bid(self, hand, auction_history):
        # 1. Determine candidates
        if not auction_history:
            candidates = self.system.get("Dealer", [])
        else:
            candidates = []
            # Try specific key first (e.g. "2C - 2D - 2H")
            full_key = self._get_key_from_auction(auction_history)
            if full_key in self.system:
                candidates = self.system.get(full_key, [])
            
            # Fallback to last bid only (e.g. "2H")
            if not candidates:
                last_bid = auction_history[-1]
                candidates = self.system.get(last_bid, [])

        # 2. Find ALL valid bids
        valid_bids = []
        for node in candidates:
            is_fit, upgrade_msg = self._does_hand_fit(hand, node.get('constraints', {}))
            if is_fit:
                node['_temp_alert'] = upgrade_msg 
                valid_bids.append(node)

        if not valid_bids:
            return BidResult("Pass", "No suitable bid found.")

        # 3. Apply Priority Logic
        best_node = self._pick_best_node(hand, valid_bids)
        
        return BidResult(
            bid=best_node['bid'],
            explanation=best_node.get('explanation', ""),
            alert=best_node.get('_temp_alert')
        )

    def _pick_best_node(self, hand, valid_nodes):
        choices = {n['bid']: n for n in valid_nodes}
        bids = list(choices.keys())

        # Specific Conventions check
        if "3C" in bids and "Second Negative" in choices["3C"].get("convention", ""):
            return choices["3C"]

        # Standard Priority: Majors > NT > Minors
        if "1S" in bids: return choices["1S"]
        if "1H" in bids: return choices["1H"]
        if "1NT" in bids: return choices["1NT"]

        # Better Minor Tie-Breaker (1C vs 1D)
        if "1C" in bids and "1D" in bids:
            d_len = hand.length_of('D')
            c_len = hand.length_of('C')
            if d_len >= 4 and c_len >= 4: return choices["1D"]
            if d_len == 3 and c_len == 3: return choices["1C"]
            if d_len > c_len: return choices["1D"]
            return choices["1C"]

        return valid_nodes[0]

    def _get_key_from_auction(self, auction):
        active_bids = [b for b in auction if b != "Pass"]
        if len(active_bids) == 0: return "Dealer"
        return " - ".join(active_bids)

    def _does_hand_fit(self, hand, constraints):
        min_hcp = constraints.get('min_hcp', 0)
        max_hcp = constraints.get('max_hcp', 40)
        upgrade_alert = None

        # --- QUALITY UPGRADE LOGIC ---
        if hand.hcp < min_hcp:
            # Allow 1 point upgrade if quality is high
            if hand.hcp == min_hcp - 1 and hand.quality_hcp >= min_hcp:
                upgrade_alert = f"Hand upgraded from {hand.hcp} to {min_hcp} due to quality ({hand.quality_hcp:.2f})."
            else:
                return False, None
        elif hand.hcp > max_hcp:
            return False, None
        # -----------------------------

        shape_req = constraints.get('shape_requirements', "")
        
        if "Balanced" in shape_req and not hand.is_balanced:
            return False, None

        matches = re.findall(r"(\d+)\+\s*(\w+)", shape_req)
        for count_str, suit_name in matches:
            min_len = int(count_str)
            suit_char = suit_name[0].upper()
            if hand.length_of(suit_char) < min_len:
                return False, None

        if "No 5-card Major" in shape_req:
            if hand.length_of('S') >= 5 or hand.length_of('H') >= 5:
                return False, None
        
        if "<3 Spades" in shape_req and hand.length_of('S') >= 3:
            return False, None

        return True, upgrade_alert