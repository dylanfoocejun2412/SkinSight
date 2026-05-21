import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

# Dictionary to map lesion types to human-readable labels
lesion_type_dict = {
    'nv': 'Melanocytic nevi',
    'mel': 'Melanoma',
    'bkl': 'Benign keratosis-like lesions',
    'bcc': 'Basal cell carcinoma',
    'akiec': 'Actinic keratoses',
    'vasc': 'Vascular lesions',
    'df': 'Dermatofibroma'
}

# Load the trained model
def load_model():
    """Load the trained model from the model directory."""
    return tf.keras.models.load_model('model/lesion_model.h5')

# Preprocess the image to match training preprocessing
def preprocess_image(image):
    """Resize and normalize the image to match the training data preprocessing."""
    # Resize the image to (100, 100) as done during training
    image = cv2.resize(image, (100, 100))

    # Normalize pixel values to the range [0, 1]
    image = image / 255.0

    # Add a batch dimension (needed for prediction)
    return np.expand_dims(image, axis=0)

# Predict the lesion type and confidence scores
def predict(image, model):
    """Predict the class of the image using the loaded model."""
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)[0]

    # Normalize predictions to ensure they sum to 1
    predictions = predictions / np.sum(predictions)

    # Get the predicted class and its confidence
    predicted_class = np.argmax(predictions)
    confidence = predictions[predicted_class] * 100

    # Get the human-readable label for the prediction
    prediction_label = list(lesion_type_dict.keys())[predicted_class]

    # Create a list of all lesion types with their confidence scores
    confidence_scores = {
        lesion_type_dict[label]: round(score * 100, 2)
        for label, score in zip(lesion_type_dict.keys(), predictions)
    }

    # Sort the confidence scores in descending order
    sorted_confidence_scores = dict(sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True))

    return lesion_type_dict[prediction_label], confidence, sorted_confidence_scores
