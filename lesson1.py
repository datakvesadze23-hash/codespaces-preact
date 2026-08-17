import streamlit as st
import base64
from groq import Groq
from pypdf import PdfReader

# Page Setup
st.set_page_config(page_title="Velox AI Assistant", page_icon="⚡", layout="wide")

# HARDCODED API KEY
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Custom Styling
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 20px;
    }
    .user-msg {
        align-self: flex-end;
        background-color: #f0f2f6;
        color: #000000;
        padding: 12px 18px;
        border-radius: 18px 18px 2px 18px;
        max-width: 70%;
    }
    .bot-msg {
        align-self: flex-start;
        background-color: #e8f0fe;
        color: #000000;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 2px;
        max-width: 70%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Velox AI Assistant")

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # თუ ბოტის პასუხია, ვუმატებთ მუშა Copy/Share ღილაკებს
        if message["role"] == "assistant":
            col1, col2 = st.columns([1, 4])
            with col1:
                # Copy ღილაკი JS კლიპბორდით
                escaped_text = message["content"].replace("`", "\\`").replace('"', '\\"')
                copy_code = f"""
                <button onclick="navigator.clipboard.writeText(`{escaped_text}`); alert('კოპირებულია!');" 
                        style="background: transparent; border: 1px solid #ccc; border-radius: 6px; padding: 4px 10px; cursor: pointer;">
                    📋 Copy
                </button>
                """
                st.components.v1.html(copy_code, height=45)

# Chat Input
if prompt := st.chat_input("ჩაწერე შეკითხვა..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()