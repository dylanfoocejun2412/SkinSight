import streamlit as st

def run():
    st.title("Welcome to SkinSight!")
    st.subheader("See beneath the surface with AI-driven skin lesion analysis.")
    st.write("""
        This app helps you classify skin lesions using advanced AI models. 
        Upload an image of a skin lesion to receive a detailed classification report, 
        including confidence levels and medical recommendations.
    """)

    st.write("### Features:")
    st.write("- 📷 **Image Classification**: Upload a skin lesion image for classification.")
    st.write("- 📜 **Classification History**: View your past classification reports.")
    st.write("- 💬 **Chatbot**: Chat with SkinGPT for additional assistance.")
    st.write("- 💬 **Statistics**: View real-time statistics by lesion type.")
    
    st.write("---")
    st.write("Use the sidebar to navigate through the app features.")

