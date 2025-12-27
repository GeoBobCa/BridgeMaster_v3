# VERSION: 2.0 (Dec 28, 2025) - Safe Text Appending (No Ruamel Corruption)
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MAIN_FILE = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")

def add_node_to_tree(key_name, yaml_text_block):
    if not os.path.exists(MAIN_FILE):
        print(f"Error: Main file not found at {MAIN_FILE}")
        return False
    
    with open(MAIN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    check_key = f'"{key_name}":'
    if check_key in content:
        print(f"⚠️  Warning: Logic for {key_name} already exists. Skipping append.")
        return False

    indented_lines = []
    for line in yaml_text_block.strip().split('\n'):
        indented_lines.append("  " + line)
    
    new_entry = f'\n\n"{key_name}":\n' + "\n".join(indented_lines) + "\n"

    print(f"Appending logic for '{key_name}' to bottom of file...")
    try:
        with open(MAIN_FILE, 'a', encoding='utf-8') as f:
            f.write(new_entry)
        print(f"Success! '{key_name}' added safely.")
        return True
    except Exception as e:
        print(f"Error appending to file: {e}")
        return False