import unittest
import sys
import os

# Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from bridge_engine import BiddingEngine, BridgeHand

class TestSpadeSystem(unittest.TestCase):
    
    def setUp(self):
        system_file = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
        self.engine = BiddingEngine(system_file)

    # --- OPENING BID TESTS ---

    def test_open_1S_standard(self):
        """Standard Opening: 13 HCP, 5 Spades"""
        hand = BridgeHand("AKJ42", "K32", "Q32", "32")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1S", "Should open 1S with 5 spades")

    def test_prefer_1S_over_1H(self):
        """Priority Check: 5 Spades and 5 Hearts -> Open 1S (Higher ranking)"""
        hand = BridgeHand("AKJ42", "AKJ42", "32", "2")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1S", "With 5-5 Majors, open the higher ranking suit (1S)")

    # --- RESPONSE TESTS (Partner Opened 1S) ---

    def test_response_2S_simple_raise(self):
        """Simple Raise: 6-9 HCP, 3 Spades"""
        # J(1)+K(3)+Q(2) = 6 HCP
        hand = BridgeHand("K43", "J32", "Q432", "432") 
        auction = ["1S"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2S", "Should be a simple raise")

    def test_response_3S_limit_raise(self):
        """Limit Raise: 10-12 HCP, 3 Spades"""
        # A(4)+Q(2)+K(3)+Q(2) = 11 HCP
        hand = BridgeHand("K43", "AQ2", "Q432", "432") 
        auction = ["1S"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "3S", "Should be a limit raise")

    def test_response_jacoby_2nt(self):
        """Jacoby 2NT: 13+ HCP, 4+ Spades"""
        # A(4)+K(3) + K(3)+J(1) + A(4) = 15 HCP
        hand = BridgeHand("KJ42", "AK2", "A432", "32") 
        auction = ["1S"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2NT", "Should bid Jacoby 2NT (Game Forcing)")

    def test_response_1nt_semiforcing(self):
        """1NT Response: 6-12 HCP, No Support"""
        hand = BridgeHand("42", "432", "KJ32", "Q432") 
        auction = ["1S"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "1NT", "Standard 1NT response")

    def test_response_2H_new_suit(self):
        """New Suit: 1S - 2H (10+ HCP, 5+ Hearts)"""
        hand = BridgeHand("42", "AKJ42", "K432", "32") # 12 HCP
        auction = ["1S"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2H", "Should show hearts naturally (Forcing)")

if __name__ == '__main__':
    unittest.main(verbosity=2)