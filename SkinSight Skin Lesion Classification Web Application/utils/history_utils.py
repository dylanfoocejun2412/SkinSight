# history_utils.py
import json
import os
from datetime import datetime

HISTORY_FILE = 'data/history.json'

# Define which lesion types are malignant
MALIGNANT_TYPES = ["Melanoma", "Basal cell carcinoma", "Actinic keratoses"]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_to_history(image_name, prediction, confidence, user_advice, doctor_advice):
    history = load_history()

    # Determine if the lesion is benign or malignant
    classification = "Malignant" if prediction in MALIGNANT_TYPES else "Benign ✅"

    new_entry = {
        'image_name': image_name,
        'image_path': f'data/uploads/{image_name}',
        'prediction': prediction,
        'confidence': round(confidence, 2),
        'classification': classification,
        'advice': user_advice,
        'doctor_advice': doctor_advice,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    history.append(new_entry)
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

