# VERSION: 4.0 (Dec 28, 2025) - Fixes Priorities (Raises > NT) and Negative Constraints (<3 Hearts)
import os
import re
from ruamel.yaml import YAML

class BidResult:
    def __init__(self, bid, explanation=None, alert=None):
        self.bid = bid
        self.explanation = explanation
        self.alert = alert
    def __str__(self): return self.bid

class BridgeHand:
    def __init__(self, s, h, d, c):
        self.suits = {'S':self._p(s), 'H':self._p(h), 'D':self._p(d), 'C':self._p(c)}
        self.hcp = self._calc_hcp()
        self.quality_hcp = self._calc_qual()
        self.distribution = {s: len(cards) for s, cards in self.suits.items()}
        self.is_balanced = sorted(self.distribution.values()) in [[3,3,3,4], [2,3,4,4], [2,3,3,5]]

    def _p(self, c_str): return list(c_str.replace(" ", "").upper())
    
    def _calc_hcp(self):
        val = {'A':4, 'K':3, 'Q':2, 'J':1}
        return sum(val.get(c,0) for s in self.suits.values() for c in s)

    def _calc_qual(self):
        val = {'A':4.5, 'K':3.0, 'Q':1.5, 'J':0.75, 'T':0.25}
        total = 0.0
        for s in self.suits.values():
            for c in s:
                if c in val: total += val[c]
                elif c == '1' and '0' in s: total += 0.25
        return total

    def length_of(self, suit): return self.distribution.get(suit, 0)

class BiddingEngine:
    def __init__(self, system_path):
        self.yaml = YAML()
        with open(system_path, 'r', encoding='utf-8') as f:
            self.system = self.yaml.load(f)

    def find_bid(self, hand, auction):
        if not auction: candidates = self.system.get("Dealer", [])
        else:
            full_key = " - ".join([b for b in auction if b != "Pass"]) or "Dealer"
            candidates = self.system.get(full_key, [])
            if not candidates and auction:
                candidates = self.system.get(auction[-1], [])

        valid_bids = []
        for node in candidates:
            fit, alert = self._does_hand_fit(hand, node.get('constraints', {}))
            if fit:
                node['_temp_alert'] = alert
                valid_bids.append(node)

        if not valid_bids: return BidResult("Pass", "No suitable bid.")
        
        best = self._pick_best_node(hand, valid_bids)
        return BidResult(best['bid'], best.get('explanation'), best.get('_temp_alert'))

    def _pick_best_node(self, hand, nodes):
        choices = {n['bid']: n for n in nodes}
        bids = list(choices.keys())

        # 1. SPECIAL CONVENTIONS
        if "3C" in bids and "Second Negative" in choices["3C"].get("convention",""): return choices["3C"]
        if "2NT" in bids and "Jacoby" in choices["2NT"].get("convention",""): return choices["2NT"]

        # 2. RAISES (SUPPORT) > NT
        # If we can raise partner (2H/3H/4H/2S/3S/4S), do that before 1NT
        for raise_bid in ["2H", "3H", "4H", "2S", "3S", "4S"]:
            if raise_bid in bids: return choices[raise_bid]

        # 3. NATURAL SUITS > NT
        if "1S" in bids: return choices["1S"]
        if "1H" in bids: return choices["1H"]
        
        # 4. NT IS LAST RESORT FOR MAJORS
        if "1NT" in bids: return choices["1NT"]

        # 5. MINORS
        if "1C" in bids and "1D" in bids:
            if hand.length_of('D') >= 4 and hand.length_of('C') >= 4: return choices["1D"]
            if hand.length_of('D') == 3 and hand.length_of('C') == 3: return choices["1C"]
            return choices["1D"] if hand.length_of('D') > hand.length_of('C') else choices["1C"]
            
        return nodes[0]

    def _does_hand_fit(self, hand, constraints):
        min_hcp = constraints.get('min_hcp', 0)
        max_hcp = constraints.get('max_hcp', 40)
        
        # Quality Upgrade
        alert = None
        if hand.hcp < min_hcp:
            if hand.hcp == min_hcp - 1 and hand.quality_hcp >= min_hcp:
                alert = f"Upgraded {hand.hcp} to {min_hcp} (Quality {hand.quality_hcp:.2f})"
            else: return False, None
        elif hand.hcp > max_hcp: return False, None

        shape_req = constraints.get('shape_requirements', "")
        
        # Regex for "X+ Suit" (Minimum Length)
        # Ignores text starting with "No " or "<" to avoid false positives
        pos_matches = re.findall(r"(?<!No )(?<!<)(\d+)\+\s*(\w+)", shape_req)
        for count, suit in pos_matches:
            if hand.length_of(suit[0].upper()) < int(count): return False, None

        # Regex for "<X Suit" (Maximum Length)
        neg_matches = re.findall(r"<(\d+)\s*(\w+)", shape_req)
        for count, suit in neg_matches:
            if hand.length_of(suit[0].upper()) >= int(count): return False, None
            
        # Legacy/Text Checks
        if "Balanced" in shape_req and not hand.is_balanced: return False, None
        if "No 5-card Major" in shape_req and (hand.length_of('H')>=5 or hand.length_of('S')>=5): return False, None

        return True, alert