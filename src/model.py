import os
import pandas as pd
import pytesseract
from PIL import Image
from tqdm import tqdm
import re
import constants
from concurrent.futures import ProcessPoolExecutor, as_completed

# Ensure Tesseract is in your PATH or set it explicitly
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Uncomment and set path if needed

def extract_text_from_image(image_path):
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")
        return ""

def extract_entity_value(text, entity_name):
    allowed_units = constants.entity_unit_map[entity_name]
    pattern = r'\b(\d+(?:\.\d+)?)\s*(' + '|'.join(map(re.escape, allowed_units)) + r')\b'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        value, unit = matches[0]
        return f"{float(value):.2f} {unit.lower()}"
    return ""

def process_image(args):
    index, image_filename, entity_name, image_folder = args
    image_path = os.path.join(image_folder, image_filename)
    if os.path.exists(image_path):
        extracted_text = extract_text_from_image(image_path)
        prediction = extract_entity_value(extracted_text, entity_name)
        return {'index': index, 'prediction': prediction}
    else:
        print(f"Image not found: {image_path}")
        return {'index': index, 'prediction': ""}

def process_images_parallel(df, image_folder, max_workers=None):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for index, row in df.iterrows():
            image_filename = os.path.basename(row['image_link'])
            args = (row['index'], image_filename, row['entity_name'], image_folder)
            futures.append(executor.submit(process_image, args))
        
        results = []
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing images"):
            results.append(future.result())
    
    return pd.DataFrame(results)

if __name__ == "__main__":
    DATASET_FOLDER = 'dataset/'
    IMAGE_FOLDER = 'images/'
    
    # Load test data
    test_df = pd.read_csv(os.path.join(DATASET_FOLDER, 'test.csv'))
    
    # Process images and extract entity values
    print("Processing images and extracting entity values...")
    results_df = process_images_parallel(test_df, IMAGE_FOLDER)
    
    # Save results
    output_filename = os.path.join(DATASET_FOLDER, 'test_out.csv')
    results_df.to_csv(output_filename, index=False)
    print(f"Results saved to {output_filename}")
    
    # Run sanity check
    print("Running sanity check...")
    from sanity import sanity_check
    sanity_check(os.path.join(DATASET_FOLDER, 'test.csv'), output_filename)