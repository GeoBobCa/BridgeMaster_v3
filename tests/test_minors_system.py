import unittest
import sys
import os

# Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from bridge_engine import BiddingEngine, BridgeHand

class TestMinorSystem(unittest.TestCase):
    
    def setUp(self):
        system_file = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
        self.engine = BiddingEngine(system_file)

    # --- OPENING BIDS ---

    def test_open_1D_natural(self):
        """13 HCP, 4 Diamonds, No 5-card Major"""
        hand = BridgeHand("K432", "Q32", "AKJ4", "32")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1D", "Should open 1D with 4 diamonds")

    def test_open_1C_natural(self):
        """13 HCP, 4 Clubs, No 5-card Major"""
        hand = BridgeHand("K432", "Q32", "32", "AKJ4")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1C", "Should open 1C with 4 clubs")

    def test_prefer_1D_with_4_4(self):
        """With 4 Diamonds and 4 Clubs, open 1D"""
        hand = BridgeHand("K32", "42", "AQJ4", "KQJ4") # 14 HCP, 4-4 Minors
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1D", "With 4-4 minors, prefer 1D")

    def test_prefer_1C_with_3_3(self):
        """With 3 Diamonds and 3 Clubs (and 4-3 Majors), open 1C"""
        # 4 Spades, 3 Hearts, 3 Diamonds, 3 Clubs -> Too strong for Pass, too unbalanced for 1NT?
        # Actually 4-3-3-3 is balanced, so this might go 1NT if 15-17.
        # Let's make it 12 HCP so it CANNOT be 1NT.
        hand = BridgeHand("AJ43", "K43", "Q32", "K32") # 12 HCP
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1C", "With 3-3 minors (Better Minor), prefer 1C")

    # --- RESPONSES (Simple) ---
    
    def test_response_1D_1H(self):
        """Partner 1D -> We have 4+ Hearts, 6+ HCP"""
        hand = BridgeHand("432", "AKJ4", "432", "432")
        auction = ["1D"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "1H", "Should show Major suit immediately")

    def test_response_1C_1S(self):
        """Partner 1C -> We have 4+ Spades, 6+ HCP"""
        hand = BridgeHand("AKJ4", "432", "432", "432")
        auction = ["1C"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "1S", "Should show Major suit immediately")

if __name__ == '__main__':
    unittest.main(verbosity=2)