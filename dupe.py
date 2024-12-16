import os
import hashlib

def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def rename_files_to_uppercase(folder):
    """Rename all files in a folder to have uppercase names, excluding the extension."""
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)
            new_name = f"{name.upper()}{ext}"  # Convert the name to uppercase, retain the extension
            new_path = os.path.join(root, new_name)

            if file_path != new_path:  # Check if the name needs to be changed
                try:
                    os.rename(file_path, new_path)
                    print(f"Renamed: {file_path} -> {new_path}")
                except Exception as e:
                    print(f"Error renaming {file_path}: {e}")

def find_duplicates(folder):
    """Find duplicate files in a folder based on SHA-256 hash."""
    file_hashes = {}  # Map of SHA-256 hash to file paths
    duplicates = []   # List of duplicate file pairs

    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_hash = calculate_sha256(file_path)
                if file_hash in file_hashes:
                    duplicates.append((file_path, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = file_path
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    return duplicates

def delete_longer_filename(duplicates):
    """Delete the file with the longer filename for each duplicate pair."""
    for file1, file2 in duplicates:
        # Compare filename lengths
        if len(file1) > len(file2):
            to_delete, to_keep = file1, file2
        else:
            to_delete, to_keep = file2, file1

        # Attempt to delete the longer file
        try:
            os.remove(to_delete)
            print(f"Deleted: {to_delete} (kept: {to_keep})")
        except Exception as e:
            print(f"Error deleting {to_delete}: {e}")

# Main script
if __name__ == "__main__":
    folder = input("Enter the folder to process: ").strip()
    if not os.path.isdir(folder):
        print("Error: Invalid folder path.")
    else:
        print(f"Processing folder: {folder}...")

        # Step 1: Rename files to uppercase
        print("Renaming files to uppercase (excluding extensions)...")
        rename_files_to_uppercase(folder)

        # Step 2: Find duplicates
        print("Scanning for duplicate files...")
        duplicates = find_duplicates(folder)

        if not duplicates:
            print("No duplicate files found.")
        else:
            print(f"Found {len(duplicates)} sets of duplicates.")
            delete_longer_filename(duplicates)