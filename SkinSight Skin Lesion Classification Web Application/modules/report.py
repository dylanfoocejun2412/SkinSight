# report.py
import streamlit as st
from utils import history_utils

def run():
    st.subheader("Classification Report")
    
    # Get the record ID from the URL
    record_id = st.experimental_get_query_params().get('id', [None])[0]
    
    if record_id:
        history = history_utils.load_history()
        record = next((item for item in history if item['id'] == record_id), None)
        
        if record:
            st.write(f"### Image: {record['image_name']}")
            st.write(f"**Predicted Lesion:** {record['prediction']}")
            st.write(f"**Confidence:** {record['confidence']:.2f}%")
            st.write(f"**Advice:** {record['advice']}")
        else:
            st.write("Report not found.")
    else:
        st.write("No report selected.")
