import streamlit as st
from ruamel.yaml import YAML
import pandas as pd
from pathlib import Path

# --- Configuration ---
st.set_page_config(page_title="BridgeMaster AI", layout="wide")

# --- Helper Functions ---
def load_rules(system_name="audrey_grant_standard"):
    """
    Loads the flat rules from YAML and converts them to a Pandas DataFrame.
    """
    # Adjust path based on where you run the command from
    rules_path = Path("systems/flat_rules.yaml")
    
    if not rules_path.exists():
        st.error(f"⚠️ Rules file not found at: {rules_path}")
        return pd.DataFrame()

    # Use Ruamel YAML for safe loading
    yaml = YAML(typ='safe') 
    with open(rules_path, "r", encoding="utf-8") as f:
        data = yaml.load(f)
    
    if not data:
        return pd.DataFrame()

    # Flatten the data for display
    rows = []
    for rule in data:
        # We only want rules for the selected system
        if rule.get("system") != system_name:
            continue
            
        # Create a readable row
        row = {
            "Auction": " - ".join(rule.get("auction", [])),
            "Bid": rule.get("bid"),
            "Min HCP": rule["constraints"].get("min_hcp"),
            "Max HCP": rule["constraints"].get("max_hcp"),
            "Shape": rule["constraints"].get("shape_requirements"),
            "Nuance (Teaching)": rule["constraints"].get("explanation"), # Short text
            "Deep Dive": rule["constraints"].get("nuance"),             # Long text
            "Source": rule["constraints"].get("source")
        }
        rows.append(row)

    return pd.DataFrame(rows)

# --- Main App Layout ---
st.title("♠️ BridgeMaster AI: System Architect")

# Create Tabs
tab1, tab2 = st.tabs(["🎮 Bidding Simulator", "🗺️ System Map"])

# --- TAB 1: Placeholder for the Simulator ---
with tab1:
    st.header("Bidding Table")
    st.info("The Bidding Simulator interface will go here. (Coming soon!)")

# --- TAB 2: The System Map (The Library) ---
with tab2:
    st.header("System Reference Library")
    
    # Load Data
    df = load_rules()
    
    if not df.empty:
        # --- Custom Column Configuration ---
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Auction": st.column_config.TextColumn(
                    "Context (Auction)",
                    width="medium",
                ),
                "Bid": st.column_config.TextColumn(
                    "Bid",
                    width="small",
                ),
                "Min HCP": st.column_config.NumberColumn(
                    "Min Pts",
                    format="%d"
                ),
                "Max HCP": st.column_config.NumberColumn(
                    "Max Pts",
                    format="%d"
                ),
                "Deep Dive": st.column_config.TextColumn(
                    "Teacher's Note (Nuance)",
                    width="large",
                    help="Detailed explanation from the source text."
                ),
                "Source": st.column_config.TextColumn(
                    "Citation",
                    width="medium"
                )
            }
        )
        
        st.caption(f"Showing {len(df)} rules from the Audrey Grant Standard system.")
    else:
        st.warning("No rules found. Please run 'src/tree_flattener.py' to generate the database.")
        