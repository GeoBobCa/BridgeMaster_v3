import unittest
import sys
import os

# Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from bridge_engine import BiddingEngine, BridgeHand

class TestNTSystem(unittest.TestCase):
    
    def setUp(self):
        system_file = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
        self.engine = BiddingEngine(system_file)

    def test_pass_weak(self):
        """Weak hand (0-7) with no long major should Pass"""
        hand = BridgeHand("J432", "432", "432", "432") # 1 HCP
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "Pass")

    def test_transfer_to_hearts(self):
        """5+ Hearts (Any points) -> Bid 2D (Transfer)"""
        # Weak hand (0 HCP) but 5 hearts
        hand = BridgeHand("432", "98765", "432", "32") 
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2D", "Should transfer to Hearts with 2D")

    def test_transfer_to_spades(self):
        """5+ Spades (Any points) -> Bid 2H (Transfer)"""
        # Strong hand (10 HCP) with 5 spades
        hand = BridgeHand("AKJ42", "432", "432", "32") 
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2H", "Should transfer to Spades with 2H")

    def test_stayman_with_hearts(self):
        """4 Hearts, 8+ HCP -> Bid 2C (Stayman)"""
        hand = BridgeHand("432", "AKJ4", "K32", "432") # 11 HCP
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2C", "Should ask for major with 2C")

    def test_stayman_with_spades(self):
        """4 Spades, 8+ HCP -> Bid 2C (Stayman)"""
        hand = BridgeHand("AKJ4", "432", "K32", "432") # 11 HCP
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2C", "Should ask for major with 2C")

    def test_invite_2nt(self):
        """8-9 HCP, Balanced, No Major -> Bid 2NT"""
        hand = BridgeHand("K32", "Q32", "K432", "432") # 8 HCP
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2NT", "Should invite with 2NT")

    def test_game_3nt(self):
        """10-15 HCP, Balanced, No Major -> Bid 3NT"""
        hand = BridgeHand("AK2", "Q32", "K432", "432") # 12 HCP
        auction = ["1NT"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "3NT", "Should bid game with 3NT")

if __name__ == '__main__':
    unittest.main(verbosity=2)