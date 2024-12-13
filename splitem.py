import os
import csv
import shutil
import random

def split_and_copy_images(csv_file, output_folder, split_ratio=0.7):
    train_folder = os.path.join(output_folder, "train")
    val_folder = os.path.join(output_folder, "val")

    # Ensure output directories exist
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)

    # Read the CSV file
    rows = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        rows = list(reader)

    # Shuffle rows and split into train/val
    random.shuffle(rows)
    split_index = int(len(rows) * split_ratio)
    train_rows = rows[:split_index]
    val_rows = rows[split_index:]

    # Helper function to copy images and write new CSV
    def copy_and_write(rows, folder, output_csv, relative_prefix):
        with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)  # Write header
            for row in rows:
                image_path = row[0]  # Assuming the first column is the image path
                if os.path.exists(image_path):
                    dest_path = os.path.join(folder, os.path.basename(image_path))
                    shutil.copy(image_path, dest_path)  # Copy image
                    row[0] = os.path.join(relative_prefix, os.path.basename(image_path))  # Update path
                    writer.writerow(row)  # Write row to new CSV
                else:
                    print(f"Warning: File not found - {image_path}")

    # Copy files and create CSVs
    copy_and_write(train_rows, train_folder, os.path.join(output_folder, "train_annotations.csv"), "train")
    copy_and_write(val_rows, val_folder, os.path.join(output_folder, "val_annotations.csv"), "val")

    print(f"Train and validation split complete. Files saved in {output_folder}")


# Main Script
if __name__ == "__main__":
    csv_file = input("Enter the path to the CSV file: ").strip()
    output_folder = input("Enter the output folder (default: 'output'): ").strip() or "output"

    if not os.path.exists(csv_file):
        print("Error: CSV file does not exist.")
    else:
        split_and_copy_images(csv_file, output_folder)