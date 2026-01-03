import streamlit as st
from ruamel.yaml import YAML
import pandas as pd
from pathlib import Path

# --- Configuration ---
st.set_page_config(page_title="BridgeMaster AI", layout="wide")

# --- Helper Functions ---
def load_all_rules():
    """
    Loads ALL rules from the flat YAML database.
    """
    rules_path = Path("systems/flat_rules.yaml")
    
    if not rules_path.exists():
        st.error(f"⚠️ Rules file not found at: {rules_path}")
        return pd.DataFrame()

    yaml = YAML(typ='safe') 
    with open(rules_path, "r", encoding="utf-8") as f:
        data = yaml.load(f)
    
    if not data:
        return pd.DataFrame()

    # Flatten logic
    rows = []
    for rule in data:
        row = {
            "System": rule.get("system"),
            "Auction": " - ".join(rule.get("auction", [])),
            "Bid": rule.get("bid"),
            "Min HCP": rule["constraints"].get("min_hcp"),
            "Max HCP": rule["constraints"].get("max_hcp"),
            "Shape": rule["constraints"].get("shape_requirements"),
            "Nuance (Teaching)": rule["constraints"].get("explanation"),
            "Deep Dive": rule["constraints"].get("nuance"),
            "Source": rule["constraints"].get("source")
        }
        rows.append(row)

    return pd.DataFrame(rows)

# --- Load Data ---
all_data_df = load_all_rules()

# --- Main Layout ---
# Use columns to put Title and Dropdown on the same row
col1, col2 = st.columns([3, 1])

with col1:
    st.title("♠️ BridgeMaster AI")

with col2:
    if not all_data_df.empty:
        # Get unique systems and sort them
        available_systems = sorted(all_data_df["System"].unique())
        
        # Set a smart default (Standard if available)
        default_index = 0
        if "audrey_grant_standard" in available_systems:
            default_index = available_systems.index("audrey_grant_standard")
            
        selected_system = st.selectbox(
            "Active System", 
            available_systems, 
            index=default_index,
            label_visibility="collapsed" # Hides the label "Active System" to save space
        )
    else:
        selected_system = "Unknown"

# Filter Data based on Dropdown
if not all_data_df.empty:
    current_df = all_data_df[all_data_df["System"] == selected_system]
else:
    current_df = pd.DataFrame()

# --- Tabs ---
tab1, tab2 = st.tabs(["🎮 Bidding Simulator", "🗺️ System Map"])

# --- TAB 1: Placeholder ---
with tab1:
    st.header(f"Bidding Table: {selected_system.replace('_', ' ').title()}")
    st.info("The Bidding Simulator interface will go here. (Coming soon!)")

# --- TAB 2: The System Map ---
with tab2:
    if not current_df.empty:
        st.dataframe(
            current_df,
            use_container_width=True,
            hide_index=True,
            height=600, # Taller table for better viewing
            column_config={
                "System": None, # Hidden
                "Auction": st.column_config.TextColumn("Context", width="medium"),
                "Bid": st.column_config.TextColumn("Bid", width="small"),
                "Min HCP": st.column_config.NumberColumn("Min", format="%d"),
                "Max HCP": st.column_config.NumberColumn("Max", format="%d"),
                "Shape": st.column_config.TextColumn("Shape", width="medium"),
                "Nuance (Teaching)": st.column_config.TextColumn("Concept", width="medium"),
                "Deep Dive": st.column_config.TextColumn(
                    "Teacher's Note",
                    width="large",
                    help="Detailed explanation."
                ),
                "Source": st.column_config.TextColumn("Citation", width="medium")
            }
        )
        st.caption(f"Showing {len(current_df)} rules for {selected_system}.")
    else:
        st.warning("No rules found. Please run 'src/tree_flattener.py'.")