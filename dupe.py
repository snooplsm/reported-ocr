import os
import hashlib
import re

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

def validate_special_naming(file_name):
    """
    Check if the file's basename starts with 't' or 'T' (or 'y'/'Y'),
    ends with 'c' or 'C', and contains exactly 6 digits in between.
    Only validate if it starts and ends with the specified letters;
    otherwise, it is considered valid.
    """
    # Only validate if the file starts with t/T or y/Y and ends with c/C
    if file_name[0].lower() in ['t', 'y'] and file_name[-1].lower() == 'c':
        # Match if there are exactly 6 digits between
        pattern = r"^[tTyY]\d{6}[cC]$"
        return re.match(pattern, file_name) is not None
    return True

def find_duplicates_and_validate(folder):
    """Find duplicate files and validate special naming rules."""
    file_hashes = {}  # Map of SHA-256 hash to file paths
    duplicates = []   # List of duplicate file pairs
    invalid_files = []  # List of files that fail the naming validation

    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            name, ext = os.path.splitext(file)

            # Validate the naming convention
            if not validate_special_naming(name):
                invalid_files.append(file_path)

            # Check for duplicates
            try:
                file_hash = calculate_sha256(file_path)
                if file_hash in file_hashes:
                    duplicates.append((file_path, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = file_path
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    return duplicates, invalid_files

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

        # Step 2: Find duplicates and validate special naming rules
        print("Scanning for duplicate files and validating naming rules...")
        duplicates, invalid_files = find_duplicates_and_validate(folder)

        # Report duplicates
        if not duplicates:
            print("No duplicate files found.")
        else:
            print(f"Found {len(duplicates)} sets of duplicates.")
            delete_longer_filename(duplicates)

        # Report invalid files
        if invalid_files:
            print(f"\nThe following files do not meet the naming criteria:")
            for invalid in invalid_files:
                print(f"- {invalid}")
        else:
            print("All files meet the naming criteria.")