import cv2
import numpy as np
import tifffile
import tensorflow as tf

def load_model(model_path):
    model = tf.keras.models.load_model(model_path)
    return model

def preprocess_image(image_path, target_size=(64, 64)):
    # Read the TIFF image
    image = tifffile.imread(image_path)
    # Convert to RGB
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Image is already in RGB format
        image_rgb = image
    else:
        # Convert single channel grayscale to RGB by replicating across all three channels
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    # Resize the image
    image_resized = cv2.resize(image_rgb, target_size)
    # Normalize the image
    image_normalized = image_resized.astype('float32') / 255.0
    # Add a batch dimension
    image_with_batch = np.expand_dims(image_normalized, axis=0)
    return image_with_batch

def predict_tumor(image_path, model):
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    predicted_class_index = np.argmax(prediction)
    
    # Define reverse mapping dictionary
    reverse_label_mapping = {0: "No Tumor", 1: "Malignant", 2: "Benign"}
    
    # Map the predicted class index to the corresponding class label
    predicted_class = reverse_label_mapping[predicted_class_index]
    
    return predicted_class
