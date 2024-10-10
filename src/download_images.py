import os
import pandas as pd
import requests
from tqdm import tqdm
from urllib.parse import urlparse
from pathlib import Path

def download_image(image_url, save_folder):
    """
    Download a single image and save it to the specified folder.
    """
    try:
        # Get the filename from the URL
        image_name = os.path.basename(urlparse(image_url).path)
        image_path = os.path.join(save_folder, image_name)

        # If image already exists, skip download
        if os.path.exists(image_path):
            return image_path

        # Download image
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return image_path
        else:
            print(f"Failed to download image: {image_url}")
            return None
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")
        return None

def download_images_from_csv(test_csv, image_folder):
    """
    Download images for all links listed in the test CSV file.
    """
    # Read CSV
    df = pd.read_csv(test_csv)
    
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
    
    for index, row in tqdm(df.iterrows(), total=len(df)):
        image_url = row['image_link']
        download_image(image_url, image_folder)

# Example usage:
if __name__ == "__main__":
    TEST_CSV = './dataset/test.csv'
    IMAGE_FOLDER = './images/'
    download_images_from_csv(TEST_CSV, IMAGE_FOLDER)
