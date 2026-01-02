import os
import sys
import json
import re
import logging
from pathlib import Path
from ruamel.yaml import YAML
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ARCHITECT")

sys.path.append(str(Path(__file__).parent))
from bridge_model import load_rules, save_rules, SUPPORTED_SYSTEMS

try:
    from google import genai
    from google.genai import types
except ImportError:
    logger.error("Library 'google-genai' not found.")
    sys.exit(1)

class SystemArchitect:
    def __init__(self, api_key, rules_file):
        self.client = genai.Client(api_key=api_key)
        self.rules_file = rules_file
        self.current_rules = load_rules(rules_file)
        
        self.definitions = {}
        def_path = rules_file.parent / "system_definitions.json"
        if def_path.exists():
            with open(def_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for sys_def in data.get("bridge_bidding_systems", []):
                    self.definitions[sys_def['system_id']] = sys_def
            logger.info(f"Loaded definitions for: {list(self.definitions.keys())}")
        else:
            logger.warning("⚠️ system_definitions.json not found! AI will fly blind.")

    def _clean_json_response(self, text):
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```json\s*", "", text)
            text = re.sub(r"^```\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        return text

    def _get_bid_value(self, bid_str):
        """Converts a bid (e.g., '1H') into an integer for comparison."""
        if bid_str.upper() == "PASS": return -1
        
        suits = {'C': 0, 'D': 1, 'H': 2, 'S': 3, 'NT': 4}
        # Parse regex: Level (1-7) + Suit (C/D/H/S/NT)
        match = re.match(r"^([1-7])(C|D|H|S|NT)$", bid_str, re.IGNORECASE)
        if not match:
            return -999
        
        level = int(match.group(1))
        suit_val = suits[match.group(2).upper()]
        
        # Formula: Level * 5 + Suit (so 1C=5, 1D=6... 1NT=9, 2C=10)
        return (level * 5) + suit_val

    def _is_valid_bid(self, bid_str):
        if bid_str.upper() == "PASS": return True
        pattern = r"^[1-7](C|D|H|S|NT)$"
        return bool(re.match(pattern, bid_str, re.IGNORECASE))

    def _is_sufficient(self, last_bid, new_bid):
        """Checks if new_bid is higher than last_bid."""
        if new_bid.upper() == "PASS": return True # You can always pass
        if not last_bid: return True # Opening bid is always sufficient
        
        val_last = self._get_bid_value(last_bid)
        val_new = self._get_bid_value(new_bid)
        
        return val_new > val_last

    def _safe_int(self, val, default=0):
        if val is None: return default
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    def generate_system_rules(self, auction_path, target_system):
        if target_system not in SUPPORTED_SYSTEMS:
            logger.error(f"System '{target_system}' is not supported.")
            return

        last_bid = auction_path[-1] if auction_path else None

        if not auction_path:
            auction_str = "No Prior Bids (Opening Seat)"
            logger.info(f"🤖 Requesting OPENING BIDS for {target_system}...")
        else:
            auction_str = ", ".join(auction_path)
            logger.info(f"🤖 Requesting responses for: {auction_str} ({target_system})...")

        sys_config = self.definitions.get(target_system, {})
        sys_config_str = json.dumps(sys_config, indent=2)

        prompt = f"""
        Act as a Bridge System Expert.
        Generate the standard set of bidding rules for:
        - Context: {auction_str}
        - System Name: {target_system}
        
        STRICT SYSTEM CONFIGURATION:
        {sys_config_str}
        
        CRITICAL INSTRUCTIONS:
        1. ADHERE STRICTLY to the configuration above.
        2. ALWAYS include a rule for "PASS" (defining the weak range).
        3. DO NOT use generic labels like "2/1", "New Suit". Expand into specific bids (2C, 2D).
        4. Capture the "flavor" of the bid in the 'nuance' field.
        5. Return ONLY a JSON object with a key "rules".
        
        Each rule object must have: 
        - bid (e.g. "2D")
        - type (Response, Rebid, etc)
        - constraints: {{ 
            min_hcp (int), 
            max_hcp (int), 
            shape_requirements (string), 
            explanation (string),
            nuance (string)
          }}
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            
            raw_text = response.text
            clean_text = self._clean_json_response(raw_text)
            data = json.loads(clean_text)
            
            new_rules = []
            for r in data.get('rules', []):
                bid_clean = r['bid'].strip().upper()

                # CHECK 1: Format
                if not self._is_valid_bid(bid_clean):
                    logger.warning(f"⚠️ REJECTED invalid format: '{bid_clean}'")
                    continue

                # CHECK 2: Sufficiency (The Fix!)
                if not self._is_sufficient(last_bid, bid_clean):
                    logger.warning(f"⚠️ REJECTED insufficient bid: '{bid_clean}' over '{last_bid}'")
                    continue

                rule_type = "Opening" if not auction_path else r.get('type', "Response")
                
                clean_rule = {
                    "auction": auction_path, 
                    "bid": bid_clean,
                    "system": target_system, 
                    "type": rule_type,
                    "constraints": {
                        "min_hcp": self._safe_int(r['constraints'].get('min_hcp')),
                        "max_hcp": self._safe_int(r['constraints'].get('max_hcp'), 37),
                        "shape_requirements": r['constraints'].get('shape_requirements', ""),
                        "explanation": r['constraints'].get('explanation', ""),
                        "nuance": r['constraints'].get('nuance', "")
                    }
                }
                new_rules.append(clean_rule)
            
            if not new_rules:
                logger.warning("⚠️ AI returned valid JSON but 0 usable rules found inside.")
            else:
                self.current_rules.extend(new_rules)
                save_rules(self.rules_file, self.current_rules)
                logger.info(f"✅ SAVED {len(new_rules)} new rules for {target_system}.")

        except json.JSONDecodeError:
            logger.error(f"❌ JSON Parse Failed. Raw text was: {raw_text[:100]}...")
        except Exception as e:
            logger.error(f"❌ General Error: {e}")

if __name__ == "__main__":
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    project_root = Path(__file__).resolve().parent.parent
    rules_path = project_root / "systems" / "flat_rules.yaml"

    if len(sys.argv) < 3:
        print("Usage: python -m src.system_architect [Auction] [System]")
    else:
        auc_arg = sys.argv[1]
        sys_arg = sys.argv[2]
        auction_list = [] if auc_arg.lower() == "opening" else [x.strip() for x in auc_arg.split(',')]
        
        architect = SystemArchitect(key, rules_path)
        architect.generate_system_rules(auction_list, sys_arg)