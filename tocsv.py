import os
import csv

import re

def remove_non_alnum(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string)  # Matches anything not a-z, A-Z, or 0-9

# Example Usage
example = "abc123!@#456_def"
result = remove_non_alnum(example)
print(result)  # Output: abc123456def
def scan_images_to_csv(directory, output_csv):
    """Scan .jpg images with filename length <= 9 and save paths and plate_text to CSV."""
    rows = []

    # Iterate through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".jpg"):  # Check if it's a .jpg file
                plate_text = os.path.splitext(file)[0]  # Extract basename (no extension)
                if len(plate_text) <= 9:  # Check if filename length (excluding .jpg) is <= 9
                    image_path = os.path.join(root, file)  # Get full path
                    rows.append([image_path, remove_non_alnum(plate_text).upper()])  # Append to rows

    # Write to CSV
    try:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["image_path", "plate_text"])  # Header
            writer.writerows(rows)
        print(f"CSV created: {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


# Main Script
if __name__ == "__main__":
    directory = input("Enter the directory to scan for images: ").strip()
    output_csv = input("Enter the output CSV file name (e.g., images.csv): ").strip()

    if not os.path.isdir(directory):
        print("Error: The specified directory does not exist.")
    else:
        scan_images_to_csv(directory, output_csv)