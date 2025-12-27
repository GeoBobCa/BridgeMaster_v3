# VERSION: 2.1 (Dec 28, 2025) - Teaching Alerts + Object Model
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

try:
    from bridge_engine import BiddingEngine, BridgeHand
except ImportError:
    print("❌ Error: Could not load 'bridge_engine.py'.")
    sys.exit(1)

def get_input_hand():
    print("\n--- NEW HAND ---")
    print("Enter cards for each suit (e.g. 'AKJ42'). Leave blank if void.")
    s = input("Spades:   ").strip()
    h = input("Hearts:   ").strip()
    d = input("Diamonds: ").strip()
    c = input("Clubs:    ").strip()
    return BridgeHand(s, h, d, c)

def main():
    system_path = os.path.join(CURRENT_DIR, "systems", "bidding_tree.yaml")
    try:
        engine = BiddingEngine(system_path)
        print("✅ System Loaded. Engine Online.")
    except Exception as e:
        print(f"❌ Failed to load system: {e}")
        return

    while True:
        try:
            hand = get_input_hand()
        except KeyboardInterrupt:
            break

        print(f"\n📊 Analysis: {hand.hcp} HCP (Standard)")
        print(f"💎 Quality:  {hand.quality_hcp:.2f} Pts")

        auction_input = input("Enter previous bids (e.g. 'Pass 1C') [Enter for None]: ").strip()
        auction_history = auction_input.split() if auction_input else []
        
        result = engine.find_bid(hand, auction_history)
        
        print(f"\n🤖 BOT RECOMMENDS: {result.bid}")
        if result.alert:
            print(f"⚠️  TEACHING ALERT: {result.alert}")
        print(f"📖 System Note: {result.explanation}")
        print("-" * 40)
        
        if input("Deal another? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()