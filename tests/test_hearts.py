import unittest
import sys
import os

# Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from bridge_engine import BiddingEngine, BridgeHand

class TestHeartSystem(unittest.TestCase):
    
    def setUp(self):
        system_file = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
        self.engine = BiddingEngine(system_file)

    # --- OPENING BID TESTS ---

    def test_open_1H_standard(self):
        """Standard Opening: 13 HCP, 5 Hearts"""
        hand = BridgeHand("K32", "AKJ42", "Q32", "32")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1H", "Should open 1H with 5 hearts and 13 HCP")

    def test_prefer_1H_over_1D(self):
        """Priority Check: 5 Hearts vs 4 Diamonds"""
        hand = BridgeHand("432", "AKJ42", "KQ32", "2")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1H", "5M should always beat 4m")

    # --- RESPONSE TESTS (Partner Opened 1H) ---

    def test_response_1S_natural(self):
        """Natural: 1H - 1S (4 Spades, 6+ HCP)"""
        hand = BridgeHand("KQ42", "42", "Q432", "432")
        auction = ["1H"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "1S", "Should show Spades naturally")

    def test_response_2H_simple_raise(self):
        """Simple Raise: 6-9 HCP, 3 Hearts"""
        # Fixed: Added a Jack to get to 6 HCP
        hand = BridgeHand("J32", "K43", "Q432", "432") 
        # Points: J(1) + K(3) + Q(2) = 6 HCP (Matches min_hcp: 6)
        auction = ["1H"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2H", "Should be a simple raise")

    def test_response_3H_limit_raise(self):
        """Limit Raise: 10-12 HCP, 3 Hearts"""
        # Fixed: Added a Queen to get to 11 HCP
        hand = BridgeHand("AQ2", "K43", "Q432", "432") 
        # Points: A(4) + Q(2) + K(3) + Q(2) = 11 HCP (Matches 10-12)
        auction = ["1H"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "3H", "Should be a limit raise")

    def test_response_jacoby_2nt(self):
        """Jacoby 2NT: 13+ HCP, 4+ Hearts"""
        # Fixed: Added a King to get to 15 HCP
        hand = BridgeHand("AK2", "KJ42", "A432", "32") 
        # Points: A(4)+K(3) + K(3)+J(1) + A(4) = 15 HCP (Matches 13+)
        auction = ["1H"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2NT", "Should bid Jacoby 2NT over 1S")

    def test_response_1nt_semiforcing(self):
        """1NT Response: 6-12 HCP, No Support, No Spades"""
        hand = BridgeHand("432", "42", "KJ32", "Q432") 
        auction = ["1H"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "1NT", "Standard 1NT response")

if __name__ == '__main__':
    unittest.main(verbosity=2)