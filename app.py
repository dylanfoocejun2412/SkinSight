import streamlit as st
from modules import home, image_classification, classification_history, chatbot, statistics

def main():
    st.sidebar.title("Menu")
    menu = ["Home", "Image Classification", "Classification History", "Chatbot", "Statistics"]
    choice = st.sidebar.selectbox("Select a Page", menu)

    if choice == "Home":
        home.run()
    elif choice == "Image Classification":
        image_classification.run()
    elif choice == "Classification History":
        classification_history.run()
    elif choice == "Chatbot":
        chatbot.run()
    elif choice == "Statistics":
        statistics.run()

if __name__ == "__main__":
    main()



