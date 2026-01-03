import json
import os
from pathlib import Path

def merge_all_systems():
    # Base directory containing the system subfolders
    base_chunks_dir = Path("systems/chunks")
    output_dir = Path("systems")
    
    if not base_chunks_dir.exists():
        print(f"❌ Error: {base_chunks_dir} does not exist.")
        return

    print(f"🏭 Starting System Factory Scan in {base_chunks_dir}...\n")

    # Loop through every SUBFOLDER in chunks (e.g., 'sayc', 'audrey_grant_basic')
    for system_folder in base_chunks_dir.iterdir():
        if system_folder.is_dir():
            system_name = system_folder.name
            output_file = output_dir / f"{system_name}_tree.json"
            
            print(f"📂 Processing System: {system_name}")
            
            merged_tree = {}
            files_count = 0
            
            # Merge all JSONs in this specific folder
            for file_path in system_folder.glob("*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            merged_tree.update(data)
                            files_count += 1
                            print(f"   + Merged chunk: {file_path.name}")
                        else:
                            print(f"   ⚠️  Skipping {file_path.name}: Root not a dict.")
                except Exception as e:
                    print(f"   ❌ Error in {file_path.name}: {e}")
            
            if files_count > 0:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(merged_tree, f, indent=2)
                print(f"   ✅ Created '{output_file.name}' from {files_count} chunks.")
            else:
                print(f"   ⚠️  No files found for {system_name}.")
            print("-" * 30)

if __name__ == "__main__":
    merge_all_systems()