import streamlit as st
import os
import cv2
from utils import model_utils, ai_advice_generator, history_utils
from jamaibase import JamAI, protocol as p

# JamAI credentials
API_KEY = "jamai_sk_dd6199ad3508babf09fcf71ab8f10e0c549f2d188c9e319b"
PROJECT_ID = "proj_64591c7c611bfa70f12f511d"
TABLE_ID_CHATBOT = "chatbot"

# Initialize JamAI client
jamai = JamAI(api_key=API_KEY, project_id=PROJECT_ID)

UPLOAD_FOLDER = 'data/uploads/'
MALIGNANT_TYPES = ["Melanoma", "Basal cell carcinoma", "Actinic keratoses"]

# Reset session state when a new image is uploaded
def reset_session():
    st.session_state.chat_history = []
    st.session_state.advice = None
    st.session_state.doctor_advice = None
    st.session_state.history_saved = False  # Reset the history saved flag

# Initialize session state variables
if "chat_history" not in st.session_state:
    reset_session()
if "advice" not in st.session_state:
    st.session_state.advice = None
if "doctor_advice" not in st.session_state:
    st.session_state.doctor_advice = None
if "history_saved" not in st.session_state:
    st.session_state.history_saved = False

def run():
    st.title("Image Classification")

    # File uploader
    uploaded_file = st.file_uploader("Upload an image to receive a skin classification report.", 
                                     type=["jpg", "png", "jpeg"], on_change=reset_session)

    if uploaded_file is not None:
        # Save the uploaded file to the uploads folder
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Load the image using OpenCV
        image = cv2.imread(image_path)
        st.image(image_path, caption="Uploaded Image", use_container_width=True)

        # Load the model and make predictions
        model = model_utils.load_model()
        prediction, confidence, confidence_scores = model_utils.predict(image, model)

        # Display predictions
        st.write(f"**Prediction:** {prediction}")
        st.write(f"**Confidence:** {confidence:.2f}%")

        # Classification status
        if prediction in MALIGNANT_TYPES:
            st.error(f"**Classification:** Malignant")
            st.warning("⚠️ This lesion is classified as malignant. Please consult a professional immediately.")
        else:
            st.success(f"**Classification:** Benign")

        # Display confidence levels
        st.subheader("Confidence Levels for All Lesion Types:")
        for lesion, score in confidence_scores.items():
            col1, col2, col3 = st.columns([2, 5, 1])
            with col1:
                st.write(f"{lesion}:")
            with col2:
                st.progress(int(score))
            with col3:
                st.write(f"{score:.2f}%")

        # --- Generate Advice ---
        if st.session_state.advice is None:
            with st.spinner("Generating advice for users..."):
                st.session_state.advice = ai_advice_generator.generate_user_advice(prediction, confidence)

        st.write("**Advice:**")
        st.success(st.session_state.advice)

        if st.session_state.doctor_advice is None:
            with st.spinner("Generating clinical recommendations..."):
                st.session_state.doctor_advice = ai_advice_generator.generate_doctor_advice(prediction, confidence)

        st.write("**Clinical Recommendations:**")
        st.info(st.session_state.doctor_advice)

        # --- Save to History (Only Once) ---
        if not st.session_state.history_saved:
            history_utils.save_to_history(
                uploaded_file.name,
                prediction,
                confidence,
                st.session_state.advice,
                st.session_state.doctor_advice
            )
            st.session_state.history_saved = True
            st.success("Classification saved to history!")

        # --- Chatbot Section ---
        st.subheader("💬 Chat with SkinGPT")

        if not st.session_state.chat_history:
            initial_message = f"The image was classified as {prediction} with a confidence of {confidence:.2f}%. Ask if they have any questions."
            completion = jamai.add_table_rows(
                table_type="action",
                request=p.RowAddRequest(
                    table_id=TABLE_ID_CHATBOT,
                    data=[{"question": initial_message}],
                    stream=False
                )
            )

            if completion.rows:
                reply_output = completion.rows[0].columns.get("reply")
                if reply_output:
                    st.session_state.chat_history.append({"role": "assistant", "content": reply_output.text})

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if chat_input := st.chat_input("Ask the assistant..."):
            st.session_state.chat_history.append({"role": "user", "content": chat_input})
            with st.chat_message("user"):
                st.write(chat_input)

            completion = jamai.add_table_rows(
                table_type="action",
                request=p.RowAddRequest(
                    table_id=TABLE_ID_CHATBOT,
                    data=[{"question": chat_input}],
                    stream=False
                )
            )

            if completion.rows:
                reply_output = completion.rows[0].columns.get("reply")
                if reply_output:
                    assistant_response = reply_output.text
                    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                    with st.chat_message("assistant"):
                        st.write(assistant_response)
                else:
                    st.error("No response from JamAI. Please try again.")
            else:
                st.error("Failed to get a response from JamAI.")
