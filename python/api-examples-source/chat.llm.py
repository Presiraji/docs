import streamlit as st
from openai import OpenAI
import os
import requests

# Set page configuration for a clean UI
st.set_page_config(page_title="FRIDAY", layout="centered")

# Title and Disclaimer
st.title("FRIDAY")
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

# Cool stock market features
st.sidebar.title("Cool Stock Market Features")

# Function to get stock data
def get_stock_data(symbol):
    api_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={st.secrets['FINNHUB_API_KEY']}"
    response = requests.get(api_url)
    return response.json()

# Input for stock symbol
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL")
if stock_symbol:
    data = get_stock_data(stock_symbol)
    st.sidebar.metric("Current Price", f"${data['c']}")
    st.sidebar.metric("High Price of the day", f"${data['h']}")
    st.sidebar.metric("Low Price of the day", f"${data['l']}")
    st.sidebar.metric("Open Price", f"${data['o']}")
    st.sidebar.metric("Previous Close Price", f"${data['pc']}")

# Displaying historical stock prices
st.sidebar.subheader("Historical Stock Prices")
history_days = st.sidebar.slider("Days", min_value=1, max_value=30, value=7)

def get_historical_data(symbol, days):
    api_url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&count={days}&token={st.secrets['FINNHUB_API_KEY']}"
    response = requests.get(api_url)
    return response.json()

if stock_symbol:
    historical_data = get_historical_data(stock_symbol, history_days)
    st.sidebar.line_chart(historical_data["c"], height=200, use_container_width=True)

# News Section
st.sidebar.subheader("Latest Stock News")
news_symbol = st.sidebar.text_input("Enter News Symbol", value="AAPL")
if news_symbol:
    news_api_url = f"https://finnhub.io/api/v1/news?category=general&token={st.secrets['FINNHUB_API_KEY']}"
    news_response = requests.get(news_api_url)
    news_data = news_response.json()
    for article in news_data[:5]:
        st.sidebar.write(f"**{article['headline']}**")
        st.sidebar.write(f"*{article['source']}*")
        st.sidebar.write(article['summary'])
        st.sidebar.write(f"[Read more]({article['url']})")
        st.sidebar.write("---")
