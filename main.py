import os
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
from insightface.app import FaceAnalysis
from generate_report import create_report
from PIL import Image

# Define directories for valid and verification images
VALID_DIR = 'valid'
VERIFICATION_DIR = 'verification'

# Initialize InsightFace
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))  # Det_size can be adjusted

def load_image(image_path):
    """Loads an image and preprocesses it to avoid format warnings."""
    # Open and re-save the image using Pillow to remove any metadata issues
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Convert to RGB if it’s not already
        img.save(image_path)  # Re-save to update format

    # Load the cleaned image with OpenCV
    img = cv2.imread(image_path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def get_embedding(image_path, scale_factor=1.0):
    """Get the face embedding for a given image path with optional scaling."""
    img = load_image(image_path)

    # Resize image to apply scaling if needed
    if scale_factor != 1.0:
        width = int(img.shape[1] * scale_factor)
        height = int(img.shape[0] * scale_factor)
        img = cv2.resize(img, (width, height))

    faces = app.get(img)
    
    if len(faces) > 0:
        return faces[0].embedding
    else:
        print(f"No face detected in image: {image_path}")
        return None
def match_verification_with_valid(scale_factor=1.0, similarity_threshold=0.6):
    """Match each image in verification subfolders with the corresponding valid image."""
    results = {}

    for person_id in os.listdir(VERIFICATION_DIR):
        person_folder = os.path.join(VERIFICATION_DIR, person_id)
        
        # Check if there is a valid image for this person
        valid_img_path = os.path.join(VALID_DIR, f"{person_id}.jpg")
        
        if not os.path.exists(valid_img_path):
            print(f"No valid image found for ID {person_id}")
            continue
        
        # Get the embedding for the valid image
        valid_embedding = get_embedding(valid_img_path, scale_factor)
        
        if valid_embedding is None:
            print(f"No face detected in valid image: {valid_img_path}")
            continue
        
        # Initialize dictionary to hold similarity results for this person ID
        results[person_id] = {
            "matched_images": {},  # To store matched images and their similarity scores
            "match_count": 0       # To count the number of matched images
        }

        # Process each image in the person's verification folder
        for img_file in os.listdir(person_folder):
            img_path = os.path.join(person_folder, img_file)
            verification_embedding = get_embedding(img_path, scale_factor)

            if verification_embedding is not None:
                similarity = cosine_similarity([valid_embedding], [verification_embedding])[0][0]
                
                if similarity >= similarity_threshold:
                    # Add matched image and similarity to results and increment match count
                    results[person_id]["matched_images"][img_file] = similarity
                    results[person_id]["match_count"] += 1
                    print(f"Similarity for {img_file} in {person_id} folder with valid image: {similarity:.4f}")
                else:
                    print(f"{img_file} in {person_id} folder is below threshold with similarity: {similarity:.4f}")
            else:
                print(f"No face detected in verification image: {img_path}")
    
    return results

def main():
    scale_factor = 1.2  # Adjust the scaling factor based on your data
    similarity_threshold = 0.5  # Set a threshold for acceptable similarity scores
    results = match_verification_with_valid(scale_factor, similarity_threshold)
    create_report(results)
    for person_id, data in results.items():
        print(f"Results for {person_id}:")
        print(f"  Total matched images: {data['match_count']}")
        
        if data["matched_images"]:
            for img_file, score in data["matched_images"].items():
                print(f"  {img_file}: Similarity score = {score:.4f}")
        else:
            print("  No images matched the similarity threshold.")

if __name__ == "__main__":
    main()
