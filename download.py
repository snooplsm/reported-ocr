import os
import csv
import hashlib
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_duplicate(file_path, existing_hashes):
    """Check if file hash exists in the existing hashes."""
    file_hash = calculate_hash(file_path)
    return file_hash in existing_hashes, file_hash

def download_image(url, output_folder, existing_hashes):
    """Download an image from a URL and check for duplicates."""
    try:
        # Extract filename from URL
        filename = url.split("/")[-1]
        output_path = os.path.join(output_folder, filename)

        # Skip if file already exists
        if os.path.exists(output_path):
            print(f"Skipping existing file: {filename}")
            return None

        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save to file
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        # Check for duplicates
        duplicate, file_hash = is_duplicate(output_path, existing_hashes)
        if duplicate:
            print(f"Duplicate detected: {filename}, removing file.")
            os.remove(output_path)
            return None

        # Add hash to the existing set
        existing_hashes.add(file_hash)
        print(f"Downloaded: {filename}")
        return filename

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def main(csv_file, output_folder, year_filter="2021", max_threads=4):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load existing file hashes
    existing_hashes = set()
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        if os.path.isfile(file_path):
            existing_hashes.add(calculate_hash(file_path))

    # Read URLs from CSV
    urls = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "url" not in reader.fieldnames:
                raise ValueError("CSV must have a 'url' column.")
            for row in reader:
                url = row.get("url")
                if url and year_filter in url and url.endswith(".jpg"):
                    urls.append(url)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Download images using multithreading
    with ThreadPoolExecutor(max_threads) as executor:
        future_to_url = {executor.submit(download_image, url, output_folder, existing_hashes): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                if result:
                    print(f"Successfully downloaded: {result}")
            except Exception as e:
                print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    # Set parameters
    csv_file = input("Enter the CSV file path: ").strip()
    output_folder = input("Enter the output folder path (default: 'images'): ").strip() or "images"
    main(csv_file, output_folder)