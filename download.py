import csv
import os
import hashlib
import requests


def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def is_duplicate(file_path, output_folder):
    """Check if a file is a duplicate based on SHA-256 hash."""
    if not os.path.exists(file_path):
        return False

    file_hash = calculate_sha256(file_path)
    for existing_file in os.listdir(output_folder):
        existing_file_path = os.path.join(output_folder, existing_file)
        if os.path.isfile(existing_file_path):
            if calculate_sha256(existing_file_path) == file_hash:
                return True
    return False


def download_images_from_csv(csv_file, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    try:
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)

            # Check if 'url' column exists
            if "url" not in reader.fieldnames:
                print("Error: CSV does not contain a 'url' header.")
                return

            for row in reader:
                url = row["url"].strip()
                if not url or "2023" not in url:
                    print(f"Skipping URL (does not contain '2024'): {url}")
                    continue  # Skip empty URLs or those without "2024"

                try:
                    # Extract filename from the URL
                    filename = os.path.basename(url.split("?")[0])  # Remove query parameters
                    output_path = os.path.join(output_folder, filename)

                    # Check for duplicates
                    if is_duplicate(output_path, output_folder):
                        print(f"Duplicate found. Skipping {url}")
                        continue

                    # Download the image
                    print(f"Downloading {url}...")
                    response = requests.get(url, stream=True)
                    response.raise_for_status()  # Check for HTTP errors

                    # Save the image
                    with open(output_path, "wb") as img_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            img_file.write(chunk)

                    print(f"Saved: {output_path}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to download {url}: {e}")

    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
if __name__ == "__main__":
    csv_file = input("Enter the path to the CSV file: ").strip()
    output_folder = input("Enter the folder to save images (default: 'images'): ").strip() or "images"
    download_images_from_csv(csv_file, output_folder)