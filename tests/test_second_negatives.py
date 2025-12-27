import unittest
import sys
import os

# Path Setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from bridge_engine import BiddingEngine, BridgeHand

class TestSecondNegative(unittest.TestCase):
    
    def setUp(self):
        system_file = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
        self.engine = BiddingEngine(system_file)

    def test_cheaper_minor_bust(self):
        """
        Scenario: Opener starts 2C (Strong), we bid 2D (Waiting).
        Opener rebids 2H (Hearts).
        We hold a BUST hand (0-3 HCP).
        We must bid 3C (Second Negative).
        """
        # A terrible hand: 1 HCP (Jack of Spades)
        hand = BridgeHand("J432", "876", "876", "876")
        
        # The Auction so far
        auction = ["2C", "2D", "2H"]
        
        # Ask the Engine
        bid = self.engine.find_bid(hand, auction)
        
        print(f"\nHand: {hand.hcp} HCP. Auction: {auction} -> Bot Bids: {bid}")
        
        # Assert
        self.assertEqual(bid, "3C", f"Bot failed to bid Second Negative! Got {bid}")

if __name__ == '__main__':
    unittest.main()