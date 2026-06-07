# A dermatologist can spot melanoma in seconds. Most people never see one in time.

If I showed you a photo of a mole and asked whether it was cancerous, you'd probably say "go see a doctor." Fair. But what if you're in a rural area, or you just want a second opinion before making that appointment?

Skin cancer is one of the most common cancers worldwide, and early detection makes an enormous difference in outcomes. The catch: most people can't tell a benign lesion from a malignant one just by looking. So I built something that can.

SkinSight is a web app that takes an image of a skin lesion and classifies it using a deep learning model trained on dermoscopy data. Upload a photo, get a result, see what the model thinks, and decide whether it's worth that doctor's visit.

# What it does
A CNN-based classifier trained to distinguish between lesion types including melanoma, basal cell carcinoma, and benign conditions

Built with Python and Streamlit, so it runs in the browser with no install needed

A chatbot module for follow-up questions and AI-generated advice

Classification history so you can track and review past results

# Architecture and stack
The model is a convolutional neural network trained on labelled dermoscopy data and implemented in Keras/TensorFlow. It uses transfer learning to compensate for the dataset size constraints common in medical imaging tasks.

The backend is written in Python with a modular structure. image_classification.py handles the inference pipeline, model_utils.py manages model loading and preprocessing, and ai_advice_generator.py wraps an LLM call to generate contextual advice based on the predicted class.

The frontend uses Streamlit with a multi-page layout covering Home, Image Classification, Classification History, Statistics, Chatbot, and Report. Classification results are written to history.json and surfaced in a history view with aggregated statistics, allowing results to be tracked across sessions. An integrated chatbot lets users ask follow-up questions about their result.

# Why it is non-trivial
Skin lesion classification is a genuinely hard computer vision problem. Inter-class visual similarity is high, melanoma and dysplastic nevi can look nearly identical even to experienced eyes. Intra-class variation is also significant due to differences in skin tone, image angle, lighting, and hair occlusion. Getting a model that generalises requires careful data handling, augmentation strategy, and architecture decisions, not just plugging images into a pretrained backbone.
This project covers the full pipeline from raw image input to classification, confidence scoring, AI-generated advice, and session history, all packaged into a single deployable application.
