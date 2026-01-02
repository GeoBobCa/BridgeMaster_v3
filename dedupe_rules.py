import sys
import logging
from pathlib import Path

# --- SETUP PATH ---
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir / "src"))

from bridge_model import load_rules, save_rules

# --- SETUP LOGGING ---
# format='%(message)s' keeps it clean (no timestamps needed for this utility)
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("DEDUPE")

def scan_and_fix_duplicates():
    rules_path = current_dir / "systems" / "flat_rules.yaml"
    
    if not rules_path.exists():
        logger.error(f"❌ File not found: {rules_path}")
        return

    logger.info(f"🔍 Scanning {rules_path.name}...")
    rules = load_rules(rules_path)
    initial_count = len(rules)
    
    # Map: Signature -> Rule Object
    # We maintain this map to keep only the LATEST definition of any bid.
    unique_map = {}
    duplicates_found = 0
    
    for r in rules:
        # 1. Create Unique Signature
        # Tuple allows it to be a dict key. 
        # We normalize case for Bid to catch '2d' vs '2D' duplicates.
        auction_sig = tuple(r.get('auction', []))
        sys_sig = r.get('system', 'ALL')
        bid_sig = str(r.get('bid', '')).strip().upper()
        
        signature = (sys_sig, auction_sig, bid_sig)
        
        # 2. Check for collision
        if signature in unique_map:
            duplicates_found += 1
            
            # Format nicely for display
            ctx_display = "OPENING" if not auction_sig else " -> ".join(auction_sig)
            
            logger.info(f"🗑️  Removing OLD definition:  [{sys_sig}]  {ctx_display}  :  {bid_sig}")
            
            # OPTIONAL: You could peek at the old rule vs new rule here
            # old_rule = unique_map[signature]
            # logger.info(f"      Old Explanation: {old_rule['constraints'].get('explanation')[:50]}...")
            
        # 3. Store/Overwrite
        # By always overwriting, we ensure the LAST rule in the file (the newest one) wins.
        unique_map[signature] = r

    # Convert back to list
    clean_rules_list = list(unique_map.values())
    
    print("-" * 60)
    if duplicates_found > 0:
        save_rules(rules_path, clean_rules_list)
        logger.info(f"✅ CLEANUP COMPLETE.")
        logger.info(f"   - Original count: {initial_count}")
        logger.info(f"   - Final count:    {len(clean_rules_list)}")
        logger.info(f"   - Removed:        {duplicates_found} duplicates")
    else:
        logger.info("✅ File is clean. No duplicates found.")

if __name__ == "__main__":
    scan_and_fix_duplicates()