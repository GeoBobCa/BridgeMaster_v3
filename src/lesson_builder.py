import sys
import json
import time
import logging
from pathlib import Path

# --- PATH SETUP ---
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from hand_factory import HandFactory

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("LESSON")

def hand_to_pbn(hands):
    """Converts the dictionary hand format to a PBN string (N:AK.Q... ...)"""
    pbn_parts = []
    for direction in ['N', 'E', 'S', 'W']:
        h = hands[direction]['suits']
        # PBN order is Spades, Hearts, Diamonds, Clubs
        pbn_str = f"{h['S']['cards']}.{h['H']['cards']}.{h['D']['cards']}.{h['C']['cards']}"
        pbn_parts.append(pbn_str)
    return "N:" + " ".join(pbn_parts)

def generate_lesson_pack(lesson_name, target_auction, count=5):
    # Setup paths
    rules_path = current_dir.parent / "systems" / "flat_rules.yaml"
    output_dir = current_dir.parent / "lessons"
    output_dir.mkdir(exist_ok=True) # Create folder if missing
    
    factory = HandFactory(rules_path)
    
    logger.info(f"📚 PRODUCING LESSON: {lesson_name}")
    logger.info(f"   Target Auction: {target_auction}")
    logger.info(f"   Quantity: {count} hands")
    logger.info("-" * 40)

    lesson_data = {
        "title": lesson_name,
        "date": time.strftime("%Y-%m-%d"),
        "target_sequence": target_auction,
        "examples": []
    }

    success_count = 0
    
    while success_count < count:
        # Ask Factory for a deal
        result = factory.generate_deal(target_auction)
        
        if result.get("success"):
            success_count += 1
            
            # Extract key info for the student
            # The 'explanation' is usually the last bid made
            last_bid_expl = result['explanations'][-1] if result['explanations'] else "No explanation."
            
            example = {
                "id": success_count,
                "pbn": hand_to_pbn(result['hands']),
                "auction": result['auction'],
                "hands_summary": {
                    "N_hcp": result['hands']['N']['total_hcp'],
                    "S_hcp": result['hands']['S']['total_hcp'],
                    "N_shape": result['hands']['N']['distribution'],
                    "S_shape": result['hands']['S']['distribution']
                },
                "teaching_point": last_bid_expl
            }
            
            lesson_data["examples"].append(example)
            logger.info(f"   ✅ Generated Hand #{success_count} ({result['attempts']} attempts)")
        else:
            logger.warning("   ⚠️ Failed to generate hand (Timeout).")

    # Save to JSON
    filename = f"{lesson_name.replace(' ', '_').lower()}.json"
    file_path = output_dir / filename
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(lesson_data, f, indent=2)
        
    logger.info("-" * 40)
    logger.info(f"🎉 LESSON COMPLETE. Saved to: lessons/{filename}")

if __name__ == "__main__":
    # EXAMPLE USAGE:
    # Let's generate a lesson on "Simple Major Raises"
    # We want 3 examples where the auction goes 1H -> 2H
    generate_lesson_pack(
        lesson_name="Major Suit Raises", 
        target_auction=["1H", "2H"], 
        count=3
    )