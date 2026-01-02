import streamlit as st
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

# --- SETUP PATHS ---
# Ensure we can find the modules in src/
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

# Import tools from our modules
from hand_factory import HandFactory
from system_architect import SystemArchitect
from bridge_model import load_rules, SUPPORTED_SYSTEMS

# --- CONFIG ---
st.set_page_config(page_title="BridgeMaster Workbench", layout="wide")
PROJECT_ROOT = current_dir.parent
RULES_FILE = PROJECT_ROOT / "systems" / "flat_rules.yaml"

# --- SIDEBAR ---
st.sidebar.title("BridgeMaster Architect")
st.sidebar.markdown("---")
# This dropdown now picks up your new JSON-defined system names
selected_system = st.sidebar.selectbox("Active System", SUPPORTED_SYSTEMS)

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🏭 Hand Factory", "🗺️ System Map", "🤖 Architect"])

# --- TAB 1: HAND FACTORY (The Simulator) ---
with tab1:
    st.header("Test Your Rules")
    st.caption("Simulate a deal to verify your system logic.")
    
    col1, col2 = st.columns(2)
    with col1:
        opener_bid = st.text_input("Opener's Bid", "1H")
    with col2:
        responder_bid = st.text_input("Responder's Bid", "2H")
    
    if st.button("Generate Deal", type="primary"):
        factory = HandFactory(RULES_FILE)
        target_auction = [opener_bid, responder_bid]
        
        with st.spinner(f"Simulating hands for {opener_bid} -> {responder_bid} in {selected_system}..."):
            result = factory.generate_deal(target_auction, selected_system)
        
        if result.get("success"):
            st.success(f"Match found in {result['attempts']} attempts!")
            
            h = result['hands']
            
            # Visual Layout for Hands
            c1, c2, c3 = st.columns([1, 1.5, 1])
            with c2:
                st.markdown(f"**North ({h['N']['total_hcp']} HCP)**")
                st.text(f"♠ {h['N']['suits']['S']['cards']}\n♥ {h['N']['suits']['H']['cards']}\n♦ {h['N']['suits']['D']['cards']}\n♣ {h['N']['suits']['C']['cards']}")
            
            c1, c2, c3 = st.columns([1, 1.5, 1])
            with c1:
                st.markdown(f"**West**")
                st.text(f"♠ {h['W']['suits']['S']['cards']}\n♥ ...")
            with c3:
                st.markdown(f"**East**")
                st.text(f"♠ {h['E']['suits']['S']['cards']}\n♥ ...")

            c1, c2, c3 = st.columns([1, 1.5, 1])
            with c2:
                st.markdown(f"**South ({h['S']['total_hcp']} HCP)**")
                st.text(f"♠ {h['S']['suits']['S']['cards']}\n♥ {h['S']['suits']['H']['cards']}\n♦ {h['S']['suits']['D']['cards']}\n♣ {h['S']['suits']['C']['cards']}")

            st.divider()
            st.markdown("### 🗣️ The Logic Check")
            st.code(" -> ".join(result['auction']))
            for exp in result['explanations']:
                st.info(exp)
        else:
            st.error(f"Failed: {result.get('error')}")
            if 'attempts' in result:
                st.write(f"Tried {result['attempts']} hands. Check your rules!")

# --- TAB 2: SYSTEM MAP (The Database) ---
with tab2:
    st.header("Current Rule Set")
    try:
        # Load rules using the shared bridge_model function
        rules = load_rules(RULES_FILE)
        
        if not rules:
            st.warning("No rules found. Go to the Architect tab to build some!")
        else:
            # Flatten for display
            flat_data = []
            for r in rules:
                flat_data.append({
                    "System": r.get('system'),
                    "Context": " -> ".join(r.get('auction', [])),
                    "Bid": r.get('bid'),
                    "Explanation": r.get('constraints', {}).get('explanation'),
                    "Nuance": r.get('constraints', {}).get('nuance', "") # The new Color Commentary column
                })
            
            df = pd.DataFrame(flat_data)
            
            # Filter by Sidebar selection
            df_filtered = df[df['System'] == selected_system]
            
            # Height set to 600 for better scrolling
            st.dataframe(
                df_filtered, 
                use_container_width=True, 
                hide_index=True, 
                height=600
            )
            st.caption(f"Showing {len(df_filtered)} rules for {selected_system}")
        
    except Exception as e:
        st.error(f"Could not load rules: {e}")

# --- TAB 3: ARCHITECT (The Builder) ---
with tab3:
    st.header("AI Rule Builder")
    st.markdown("Generate standard bidding rules for a specific situation.")
    
    col_a, col_b = st.columns([3, 1])
    with col_a:
        context_input = st.text_input("Target Context (e.g., '1H' or '1D, 1S')", help="Leave empty for Opening Bids")
    
    if st.button("Auto-Build Rules"):
        load_dotenv()
        key = os.getenv("GEMINI_API_KEY")
        
        if not key:
            st.error("No API Key found in .env")
        else:
            architect = SystemArchitect(key, RULES_FILE)
            auction_path = [x.strip() for x in context_input.split(',')] if context_input else []
            
            with st.status(f"Consulting Expert for {selected_system}...", expanded=True) as status:
                st.write("Reading System Constitution...")
                st.write("Drafting Rules...")
                architect.generate_system_rules(auction_path, selected_system)
                status.update(label="Build Complete!", state="complete", expanded=False)
            
            st.success(f"Done! Check the 'System Map' tab to see the new {selected_system} rules.")