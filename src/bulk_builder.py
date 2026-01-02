import time
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# --- PATH FIX ---
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))         # For system_architect (in src)
sys.path.append(str(current_dir.parent))  # For dedupe_rules (in root)

from system_architect import SystemArchitect
from dedupe_rules import scan_and_fix_duplicates

# --- SETUP LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("BUILDER")

# --- CONFIGURATION ---
TARGET_SYSTEM = "audrey_grant_standard"  # <--- New ID matches JSON

BATCH_LIST = [
    "1C",
    "1D",
    "1H",
    "1S",
    "1NT",
    "2C", 
    "2NT"
]

def run_batch():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        logger.error("❌ ERROR: No API Key found.")
        return

    # Point to the rules file (parent of src is root)
    rules_path = current_dir.parent / "systems" / "flat_rules.yaml"
    
    logger.info("=" * 60)
    logger.info(f"🚀 STARTING BATCH BUILDER")
    logger.info(f"🎯 Target System: {TARGET_SYSTEM}")
    logger.info(f"📋 Queue ({len(BATCH_LIST)} items): {BATCH_LIST}")
    logger.info("=" * 60)

    architect = SystemArchitect(key, rules_path)
    total_added = 0

    for index, auction_str in enumerate(BATCH_LIST):
        step_num = index + 1
        logger.info(f"\n🔨 [Step {step_num}/{len(BATCH_LIST)}] Architecting responses for: '{auction_str}'...")
        
        # Convert "1C" -> ["1C"]
        auction_list = [auction_str]
        
        len_before = len(architect.current_rules)
        architect.generate_system_rules(auction_list, TARGET_SYSTEM)
        len_after = len(architect.current_rules)
        
        added = len_after - len_before
        total_added += added
        
        if added > 0:
            logger.info(f"   ✨ Result: +{added} rules added for {auction_str}")
        else:
            logger.warning(f"   ⚠️ Result: No new rules added.")

        time.sleep(2)

    logger.info("\n" + "=" * 60)
    logger.info("🧹 BATCH COMPLETE. Running Auto-Dedupe cleanup...")
    
    scan_and_fix_duplicates()
    
    logger.info("=" * 60)
    logger.info(f"✅ FINAL REPORT: Added approximately {total_added} new rules.")
    logger.info("   Your system is now ready for testing.")

if __name__ == "__main__":
    run_batch()