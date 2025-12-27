# VERSION: 2.1 (Dec 28, 2025) - Object Model Compatible
import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from bridge_engine import BiddingEngine, BridgeHand

class TestOpeningBids(unittest.TestCase):
    
    def setUp(self):
        system_file = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
        self.engine = BiddingEngine(system_file)

    def test_01_pass_hand(self):
        hand = BridgeHand("J432", "432", "432", "432")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "Pass")

    def test_02_open_1nt(self):
        # 16 HCP Balanced
        hand = BridgeHand("KQ42", "KJ3", "QJ3", "K32")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1NT")

    def test_03_open_1spade(self):
        # 13 HCP, 5 Spades
        hand = BridgeHand("AKJ42", "K32", "432", "Q2")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1S")

    def test_04_open_1heart(self):
        # 14 HCP, 5 Hearts
        hand = BridgeHand("42", "AKJ42", "K32", "Q32")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1H")

    def test_05_better_minor_diamonds(self):
        # 14 HCP, 4D/4C -> 1D
        hand = BridgeHand("A32", "A32", "K432", "Q432")
        result = self.engine.find_bid(hand, [])
        self.assertEqual(result.bid, "1D")

    def test_06_stayman_rebid_neg(self):
        # 1NT - 2C - ? (No Major) -> 2D
        hand = BridgeHand("K32", "K32", "AQ32", "K32")
        auction = ["1NT", "Pass", "2C", "Pass"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "2D")

    def test_07_second_negative_bust(self):
        # 2C - 2D - 2H - ? (Bust Hand) -> 3C
        hand = BridgeHand("J432", "876", "876", "876")
        auction = ["2C", "2D", "2H"]
        result = self.engine.find_bid(hand, auction)
        self.assertEqual(result.bid, "3C")

if __name__ == '__main__':
    unittest.main(verbosity=2)