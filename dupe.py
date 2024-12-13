import os
import hashlib

def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

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

def delete_duplicates(duplicates):
    """Interactively delete one of the duplicate files."""
    for idx, (file1, file2) in enumerate(duplicates, start=1):
        print(f"\nDuplicate Set {idx}:")
        print(f"1: {file1}")
        print(f"2: {file2}")
        choice = input("Choose a file to delete (1/2) or skip (s): ").strip().lower()

        if choice == "1":
            try:
                os.remove(file1)
                print(f"Deleted: {file1}")
            except Exception as e:
                print(f"Error deleting {file1}: {e}")
        elif choice == "2":
            try:
                os.remove(file2)
                print(f"Deleted: {file2}")
            except Exception as e:
                print(f"Error deleting {file2}: {e}")
        elif choice == "s":
            print("Skipped this set.")
        else:
            print("Invalid input. Skipping this set.")

# Main script
if __name__ == "__main__":
    folder = input("Enter the folder to scan for duplicates: ").strip()
    if not os.path.isdir(folder):
        print("Error: Invalid folder path.")
    else:
        print(f"Scanning folder: {folder}...")
        duplicates = find_duplicates(folder)

        if not duplicates:
            print("No duplicate files found.")
        else:
            print(f"Found {len(duplicates)} sets of duplicates.")
            delete_duplicates(duplicates)