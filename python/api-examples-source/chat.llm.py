import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="FRIDAY", layout="wide")
st.title("FRIDAY")

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        """Do not use this
        """
    )

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "max_messages" not in st.session_state:
    st.session_state.max_messages = 100

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
