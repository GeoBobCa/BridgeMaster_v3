import streamlit as st
import sys
import json
from pathlib import Path
from ruamel.yaml import YAML

# --- SETUP ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

import hand_generator 

# --- CONFIG ---
st.set_page_config(page_title="BridgeMaster Control", layout="wide")
RULES_FILE = PROJECT_ROOT / "systems" / "flat_rules.yaml"

# --- HELPER FUNCTIONS ---
def calculate_hcp(hand_str):
    """Calculates HCP from a PBN hand string (e.g. 'AK.T9...')"""
    hcp = 0
    values = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
    clean_hand = hand_str.replace('.', '')
    for card in clean_hand:
        hcp += values.get(card, 0)
    return hcp

def render_hand(hand_str, label):
    """Renders a single hand with HCP."""
    suits = hand_str.split('.')
    symbols = ['♠', '♥', '♦', '♣'] 
    colors = ['black', 'red', 'orange', 'black'] 
    
    hcp = calculate_hcp(hand_str)
    
    st.markdown(f"**{label}** ({hcp} HCP)")
    for i, suit_holding in enumerate(suits):
        if not suit_holding: suit_holding = "—"
        color = colors[i]
        symbol = symbols[i]
        st.markdown(f":{color}[{symbol} {suit_holding}]")

def parse_pbn_deal(pbn_line):
    """Parses 'N:xxx...' into a list of 4 hands."""
    content = pbn_line.split(':')[1] 
    hands = content.split(' ')
    return hands # [North, East, South, West]

def get_auction_tree(rules):
    """Builds a hierarchy of the bidding system."""
    tree = {}
    sorted_rules = sorted(rules, key=lambda x: len(x.get('auction', [])))
    for rule in sorted_rules:
        auction_path = tuple(rule.get('auction', []))
        if auction_path not in tree: tree[auction_path] = []
        tree[auction_path].append(rule)
    return tree

# --- TABS ---
tab1, tab2 = st.tabs(["🏭 Hand Factory", "🗺️ System Map"])

with tab1:
    st.header("Generate Hands")
    
    col_input, col_action = st.columns([1, 4])
    
    with col_input:
        step1 = st.selectbox("Opener", ["1S", "1H", "1D", "1C", "1NT", "2C"], key="t1")
        step2 = st.text_input("Responder", value="2H", key="t2")
        step3 = st.text_input("Rebid", value="", key="t3")
        
        target = [step1]
        if step2: target.append(step2)
        if step3: target.append(step3)

        # "SAFETY STOP" Logic is handled inside the generator (we might need to tweak generator for max loops later, 
        # but for now Streamlit's stop button in the top right works best for hard aborts).
        if st.button("🚀 Generate", type="primary"):
            with st.spinner(f"Simulating deals to find: {target}..."):
                # Configure Generator
                hand_generator.TARGET_START = target
                hand_generator.TARGET_COUNT = 1 
                
                # Run
                hand_generator.main()
                st.session_state['generated'] = True

    with col_action:
        PBN_FILE = PROJECT_ROOT / "output" / "generated_hands.pbn"
        if PBN_FILE.exists() and st.session_state.get('generated'):
            with open(PBN_FILE, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Simple Parser
            deals = content.split('[Event "')
            for d in deals:
                if not d.strip(): continue
                
                lines = d.splitlines()
                deal_line = ""
                note_line = ""
                auction_log = []
                
                for line in lines:
                    if line.startswith('[Deal'): deal_line = line.split('"')[1]
                    if line.startswith('[Note'): note_line = line.split('"')[1]
                    if not line.startswith('[') and len(line) > 3: auction_log.append(line)

                if deal_line:
                    hands = parse_pbn_deal(deal_line)
                    
                    st.subheader("Bidding Table")
                    
                    # --- COMPASS LAYOUT ---
                    c1, c2, c3 = st.columns([1, 1, 1])
                    with c2: render_hand(hands[0], "NORTH")
                    
                    c1, c2, c3 = st.columns([1, 1, 1])
                    with c1: render_hand(hands[3], "WEST")
                    with c2: st.image("https://www.bridgebase.com/mobile/images/table_felt.png", width=150)
                    with c3: render_hand(hands[1], "EAST")
                    
                    c1, c2, c3 = st.columns([1, 1, 1])
                    with c2: render_hand(hands[2], "SOUTH")
                    
                    st.divider()
                    
                    # --- LOGIC EXPLANATION ---
                    st.write("### 🧠 Why did they bid that?")
                    if note_line:
                        steps = note_line.split(" | ")
                        for s in steps:
                            st.info(s)

                    st.divider()
                    
                    # --- DEBUG / ERROR REPORTING ---
                    with st.expander("🐞 Found a logic error? Click here."):
                        st.write("If the bot made a bad bid, describe it below and copy the data block to the AI.")
                        user_comment = st.text_input("What was wrong?", placeholder="e.g. South should have bid 3NT with 14 HCP")
                        
                        debug_data = {
                            "comment": user_comment,
                            "target_sequence": target,
                            "hands": {
                                "N": hands[0],
                                "E": hands[1],
                                "S": hands[2],
                                "W": hands[3]
                            },
                            "auction_history": auction_log,
                            "logic_trace": note_line
                        }
                        
                        st.json(debug_data)
                        st.caption("Copy the JSON block above and paste it into the chat.")

with tab2:
    st.header("System Map (Coverage)")
    if RULES_FILE.exists():
        yaml = YAML(typ='safe', pure=True)
        with RULES_FILE.open("r", encoding="utf-8") as f:
            rules = yaml.load(f)
        tree = get_auction_tree(rules)
        openings = tree.get(tuple(), [])
        
        for rule in openings:
            bid = rule['bid']
            with st.expander(f"OPENING: {bid}"):
                st.caption(rule.get('constraints', {}).get('explanation', ''))
                responses = tree.get(tuple([bid]), [])
                if not responses:
                    st.error(f"⚠️ Dead End! No responses defined for {bid}")
                else:
                    for resp in responses:
                        resp_bid = resp['bid']
                        st.markdown(f"**Response:** {resp_bid}")
                        rebids = tree.get(tuple([bid, resp_bid]), [])
                        if not rebids:
                            st.warning(f"  └── ⚠️ No Rebids defined for {bid} - {resp_bid}")
                        else:
                            for rebid in rebids:
                                st.markdown(f"  └── **Rebid:** {rebid['bid']}")
    else:
        st.error("Rules file not found!")