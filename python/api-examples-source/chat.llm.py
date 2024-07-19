import streamlit as st
from openai import OpenAI
import os

# Set page configuration for a clean UI
st.set_page_config(page_title="ChatGPT-like clone", layout="centered")

# Title and Disclaimer
st.title("ChatGPT-like clone")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        """We appreciate your engagement! Please note, this demo is designed to
        process a maximum of 10 interactions and may be unavailable if too many
        people use the service concurrently. Thank you for your understanding.
        """
    )

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    st.session_state.max_messages = 20

if "usage" not in st.session_state:
    st.session_state.usage = 0

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Usage tracking and rate limit display
st.sidebar.title("Usage Details")
st.sidebar.write(f"Usage: {st.session_state.usage} / {st.session_state.max_messages}")

if st.session_state.usage >= st.session_state.max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached. We value your interest!
        We encourage you to experience further interactions by building your own application with instructions
        from Streamlit's [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
        tutorial. Thank you for your understanding."""
    )
else:
    # Chat input and response handling
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.usage += 1

        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except:
                st.session_state.max_messages = len(st.session_state.messages)
                rate_limit_message = """
                    Oops! Sorry, I can't talk now. Too many people have used
                    this service recently.
                """
                st.session_state.messages.append(
                    {"role": "assistant", "content": rate_limit_message}
                )
                st.rerun()

# File upload feature
st.sidebar.title("Upload Files")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    st.sidebar.write(file_details)
    with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("File uploaded successfully!")
