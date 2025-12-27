import shutil
import os
import datetime

# CONFIGURATION
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_FILE = os.path.join(PROJECT_ROOT, "systems", "bidding_tree.yaml")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backups")

def create_backup():
    # 1. Ensure backup folder exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # 2. Get a label from the user
    print(f"Current System Size: {os.path.getsize(SOURCE_FILE)} bytes")
    label = input("Enter a label for this backup (e.g. 'Added 1H Opening'): ").strip()
    
    # Clean the label to be filename-safe
    safe_label = "".join([c if c.isalnum() else "_" for c in label])

    # 3. Create the filename
    # Format: 2025-12-28_14-30__Added_1H_Opening.yaml
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{timestamp}__{safe_label}.yaml"
    dest_path = os.path.join(BACKUP_DIR, filename)

    # 4. Copy
    try:
        shutil.copy2(SOURCE_FILE, dest_path)
        print(f"✅ Backup saved to: backups/{filename}")
    except Exception as e:
        print(f"❌ Backup Failed: {e}")

if __name__ == "__main__":
    create_backup()