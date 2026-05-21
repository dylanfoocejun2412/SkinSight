# classification_history.py
import streamlit as st
from utils import history_utils

def run():
    st.title("Classification History")

    # Load history from the JSON file
    history = history_utils.load_history()

    if not history:
        st.write("No classification history found.")
        return

    # Sort the history in descending order by timestamp
    history = sorted(history, key=lambda x: x['timestamp'], reverse=True)

    # Display the history as clickable items
    for index, record in enumerate(history):
        classification = record.get('classification', 'Unknown')
        classification_status = f"**Classification:** {classification}"

        if classification == "Malignant":
            classification_status += " ⚠️ **Consult a professional immediately.**"
            with st.expander(f"⚠️ {record['image_name']} - {record['prediction']} {record['confidence']:.2f}% ({record['timestamp']})"):
                st.image(record['image_path'], caption=f"Image: {record['image_name']}", use_container_width=True)
                st.write(f"**Predicted Lesion:** {record['prediction']}")
                st.write(f"**Confidence:** {record['confidence']:.2f}%")
                st.error(classification_status)
                st.write(f"**Advice:** {record['advice']}")
                st.write(f"**Clinical Recommendations:** {record.get('doctor_advice', 'No clinical recommendations available.')}")
        else:
            with st.expander(f"✅ {record['image_name']} - {record['prediction']} {record['confidence']:.2f}% ({record['timestamp']})"):
                st.image(record['image_path'], caption=f"Image: {record['image_name']}", use_container_width=True)
                st.write(f"**Predicted Lesion:** {record['prediction']}")
                st.write(f"**Confidence:** {record['confidence']:.2f}%")
                st.success(classification_status)
                st.write(f"**Advice:** {record['advice']}")
                st.write(f"**Clinical Recommendations:** {record.get('doctor_advice', 'No clinical recommendations available.')}")
