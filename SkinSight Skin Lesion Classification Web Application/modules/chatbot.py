import streamlit as st
from jamaibase import JamAI, protocol as p

# JamAI credentials
API_KEY = "jamai_sk_dd6199ad3508babf09fcf71ab8f10e0c549f2d188c9e319b"
PROJECT_ID = "proj_64591c7c611bfa70f12f511d"
TABLE_ID_CHATBOT_STANDALONE = "chatbot_standalone"  # New table for the standalone chatbot

# Initialize JamAI client
jamai = JamAI(api_key=API_KEY, project_id=PROJECT_ID)

# Store chat history in session state
if "standalone_chat_history" not in st.session_state:
    st.session_state.standalone_chat_history = [{"role": "assistant", "content": "Hello! How can I help you with your skin concerns?"}]

def run():
    st.title("💬 Chat with SkinGPT Assistant")

    # Display chat history
    for message in st.session_state.standalone_chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input box for user to type messages
    if chat_input := st.chat_input("Ask the assistant..."):
        # Save user input to chat history
        st.session_state.standalone_chat_history.append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.write(chat_input)

        # Send the user input to the new chatbot table in JamAI
        completion = jamai.add_table_rows(
            table_type="action",
            request=p.RowAddRequest(
                table_id=TABLE_ID_CHATBOT_STANDALONE,
                data=[{"question": chat_input}],
                stream=False
            )
        )

        # Get the assistant's response
        if completion.rows:
            reply_output = completion.rows[0].columns.get("reply")
            if reply_output:
                assistant_response = reply_output.text
                st.session_state.standalone_chat_history.append({"role": "assistant", "content": assistant_response})
                with st.chat_message("assistant"):
                    st.write(assistant_response)
            else:
                st.error("No response from JamAI. Please try again.")
        else:
            st.error("Failed to get a response from JamAI.")

