# **Image-Based OCR Prediction System**

This project is an **Image-Based OCR Prediction System** that extracts text from product images, particularly numbers and units (e.g., "10 kg" or "5 liters"), using Optical Character Recognition (OCR) and deep learning techniques. The system utilizes Tesseract OCR and a ResNet50-based deep learning model to predict the desired entities from images, specifically focusing on predicting numerical values and their corresponding units.

## **Table of Contents**

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Training the Model](#training-the-model)
  - [Running Predictions](#running-predictions)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## **Features**

- **OCR (Optical Character Recognition)**: Uses Tesseract to extract text from images.
- **Deep Learning**: Utilizes a ResNet50-based model for entity prediction.
- **Image Preprocessing**: Converts images to grayscale, enhances contrast, and sharpens images to improve OCR accuracy.
- **Multiprocessing for Image Downloads**: Downloads product images in parallel to speed up processing.
- **Batch Processing**: Processes images in batches for scalable prediction generation.
- **Prediction Output**: Extracts number and unit predictions (e.g., "10 kg") from OCR results and saves them to a CSV file.

## **Project Structure**

```
.
├── dataset/
│   ├── train.csv        # Training dataset CSV with image links
│   ├── test.csv         # Test dataset CSV with image links
│   ├── test_output.csv  # Generated output with predictions
│   └── images/          # Directory for downloaded images
├── src/
│   ├── constants.py     # Contains allowed units and configurations
│   ├── model.py         # Deep learning model definition and training script
│   ├── Download_Images.py  # OCR script to process test data and generate predictions
│   ├── utils.py         # Utility functions (e.g., downloading images, parsing strings)
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## **Setup**

### **Prerequisites**

Ensure the following software and libraries are installed on your system:

- Python 3.7+
- [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) (for Windows users, install it and update the path in the script)
- CUDA (Optional but recommended for GPU support)

### **Installation**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mohdmuneef/image-based-ocr-prediction-system.git
   cd image-based-ocr-prediction-system
   ```

2. **Install Dependencies**:
   Use `pip` to install the required libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Tesseract Path**:
   - For Windows users, update the path to Tesseract in `OCR_Image_Processing.py`:
     ```python
     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     ```

4. **Dataset Setup**:
   - Place your training and test data CSV files in the `dataset/` directory.
   - Ensure the `train.csv` and `test.csv` files contain columns for `image_link`, `group_id`, and `entity_name`.

## **Usage**

### **Training the Model**

To train the deep learning model using ResNet50, run the following command:

```bash
python src/model.py
```

This script will:
- Download the images specified in `dataset/train.csv`.
- Train a ResNet50 model on the dataset.
- Save the model weights to `model_weights.pth`.

### **Running Predictions**

To run OCR and prediction on the test dataset (`test.csv`), execute:

```bash
python src/Download_Images.py
```

This script will:
- Download images from `test.csv`.
- Perform OCR on the images and extract numerical entities.
- Save the results in `dataset/test_output.csv`.

## **Configuration**

- **Image Download**: Images are downloaded into the `dataset/images/` directory. Modify `IMAGE_FOLDER` in `Download_Images.py` if needed.
- **Batch Size**: The batch size for processing images is set to 100 by default. You can change this in the `generate_predictions` function in `Download_Images.py`.
- **Allowed Units**: Units allowed for extraction are defined in `constants.py` under `allowed_units`.

## **Contributing**

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

