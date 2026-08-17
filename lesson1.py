import streamlit as st
import base64
from groq import Groq
from pypdf import PdfReader
from io import BytesIO

# Page Setup
st.set_page_config(page_title="Velox AI Assistant", page_icon="⚡", layout="wide")

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# Custom CSS to hide avatars and top Streamlit header
st.markdown("""
    <style>
    /* Hide Avatars in chat messages */
    [data-testid="chatAvatarIcon-assistant"],
    [data-testid="chatAvatarIcon-user"],
    .stChatMessageAvatar {
        display: none !important;
    }
    .stApp > header { display: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Velox AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

# --- SIDEBAR (English) ---
with st.sidebar:
    st.title("Velox Control Panel")
    st.markdown("Welcome! I am **Velox AI**, your fast and smart assistant.")
    st.divider()
    
    uploaded_file = st.file_uploader("Upload PDF document for context", type="pdf")
    
    if uploaded_file is not None:
        try:
            reader = PdfReader(BytesIO(uploaded_file.read()))
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()
            st.session_state.pdf_context = pdf_text
            st.success("✅ PDF processed successfully!")
        except Exception as e:
            st.error(f"❌ Error reading PDF: {e}")
            st.session_state.pdf_context = ""
    else:
        st.session_state.pdf_context = ""

    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.pdf_context = ""
        st.rerun()

# --- CHAT DISPLAY ---
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant":
            escaped_text = message["content"].replace("`", "\\`").replace('"', '\\"')
            copy_code = f"""
            <button onclick="navigator.clipboard.writeText(`{escaped_text}`);" 
                    style="background: transparent; border: 1px solid #ccc; border-radius: 6px; padding: 4px 10px; cursor: pointer; color: black; font-size: 14px;">
                📋 Copy
            </button>
            """
            st.components.v1.html(copy_code, height=45)

# --- CHAT INPUT & RESPONSE ---
if prompt := st.chat_input("Ask something..."):
    full_prompt = prompt
    if st.session_state.pdf_context:
        full_prompt = f"--- PDF CONTEXT ---\n{st.session_state.pdf_context}\n----------------------\n\nUser Question: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Velox AI, a smart assistant. Use the provided PDF context if it exists."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]],
                {"role": "user", "content": full_prompt}
            ],
            stream=True,
        )
        
        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response + "▌")
        
        response_container.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()