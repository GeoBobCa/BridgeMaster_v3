from pathlib import Path
from ruamel.yaml import YAML

# Initialize the YAML handler
yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False

# --- UPDATED LIST TO MATCH YOUR JSON IDs ---
SUPPORTED_SYSTEMS = [
    "audrey_grant_basic",
    "audrey_grant_standard",
    "sayc",
    "sayc_2_1_gf"
]

def load_rules(file_path):
    """
    Loads rules from a YAML file using ruamel.yaml.
    Returns an empty list if file doesn't exist or is empty.
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.load(f)
            return data if data is not None else []
        except Exception as e:
            print(f"Error loading rules: {e}")
            return []

def save_rules(file_path, rules):
    """
    Saves rules to a YAML file using ruamel.yaml.
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(rules, f)