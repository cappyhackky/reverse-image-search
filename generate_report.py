import os
import csv

# Define paths to directories
VERIFICATION_DIR = "verification"
VALID_DIR = "valid"

# Function to create a report
def create_report(matching_results):
    # Define CSV file name
    report_file = "verification_report.csv"

    # Define headers for the report
    headers = [
        "Folder Name",
        "Admission Number Exists?",
        "No. of Images",
        "No. of Verified Images",
        "Data Count Remark",
        "Directory Remark",
        "Verification Status Remark",
    ]

    # Open CSV file for writing
    with open(report_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers

        # Iterate through each folder in the verification directory
        for folder_name in os.listdir(VERIFICATION_DIR):
            folder_path = os.path.join(VERIFICATION_DIR, folder_name)

            # Check if the folder is indeed a directory
            if not os.path.isdir(folder_path):
                continue

            # Admission number check: Check if a valid image exists with the same name
            valid_image_path = os.path.join(VALID_DIR, f"{folder_name}.jpg")
            admission_exists = "Yes" if os.path.exists(valid_image_path) else "No"

            # Count total images in the verification folder
            total_images = len([img for img in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, img))])
            
            # Number of verified images: retrieve from matching results
            verified_images = matching_results.get(folder_name, {}).get("match_count", 0)

            # Initialize remarks
            count_remark = "✔"
            directory_remark = "✔"
            verify_remark = "✔"

            # Add remarks based on conditions
            if total_images == 0:
                count_remark = "Empty Dataset Folder"
                verify_remark = "No Dataset"
            elif total_images not in [5, 10]:
                count_remark = "Invalid Data Count"

            if admission_exists == "No":
                directory_remark = "Verification data does not exist or Invalid directory name"
                verify_remark = "No verification data"

            if admission_exists == "Yes" and total_images > 0:
                if verified_images < total_images:
                    verify_remark = "Mixed Dataset" 
                elif verified_images == 0:
                    verify_remark = "Invalid Dataset"

            # Write data to the CSV file
            writer.writerow([
                folder_name,
                admission_exists,
                total_images,
                verified_images,
                count_remark,
                directory_remark,
                verify_remark,
            ])

    print(f"Report saved to {report_file}")