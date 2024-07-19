import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="ChatGPT-like Clone", layout="wide")
st.title("ChatGPT-like Clone")

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        """We appreciate your engagement! Please note, this demo is designed to
        process a maximum of 10 interactions and may be unavailable if too many
        people use the service concurrently. Thank you for your understanding.
        """
    )

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    st.session_state.max_messages = 20

# API Usage and Credits
if "api_usage" not in st.session_state:
    st.session_state.api_usage = 0

if "api_credits" not in st.session_state:
    st.session_state.api_credits = 100  # Assuming 100 credits initially

st.sidebar.title("Usage and Credits")
st.sidebar.write(f"API Usage: {st.session_state.api_usage}")
st.sidebar.write(f"API Credits Left: {st.session_state.api_credits}")

# File and Image Upload
st.sidebar.title("Upload Files")
uploaded_files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True)
uploaded_images = st.sidebar.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    st.sidebar.write("Uploaded Files:")
    for uploaded_file in uploaded_files:
        st.sidebar.write(f"- {uploaded_file.name}")

if uploaded_images:
    st.sidebar.write("Uploaded Images:")
    for uploaded_image in uploaded_images:
        st.sidebar.image(uploaded_image, caption=uploaded_image.name, use_column_width=True)

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) >= st.session_state.max_messages:
    st.info(
        """Notice: The maximum message limit for this demo version has been reached. We value your interest!
        We encourage you to experience further interactions by building your own application with instructions
        from Streamlit's [Build a basic LLM chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
        tutorial. Thank you for your understanding."""
    )
else:
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

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
                # Update API usage and credits
                st.session_state.api_usage += 1
                st.session_state.api_credits -= 1
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
