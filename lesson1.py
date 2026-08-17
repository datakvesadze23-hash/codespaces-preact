import streamlit as st
import base64
from groq import Groq
from pypdf import PdfReader

# Page Setup
st.set_page_config(page_title="NexusAI Assistant", page_icon="⚡", layout="wide")

# HARDCODED API KEY (რომ მომხმარებლებს ჩაწერა არ დასჭირდეთ)
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]  # <--- აქ ჩასვი შენი API Key

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
        word-wrap: break-word;
        font-size: 15px;
    }
    .ai-msg-box {
        align-self: flex-start;
        background-color: #ffffff;
        color: #000000;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 2px;
        max-width: 80%;
        word-wrap: break-word;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        font-weight: 600;
        color: #333;
        font-size: 14px;
    }
    /* Glowing Orange Dot */
    .orange-dot {
        width: 10px;
        height: 10px;
        background-color: #ff9900;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #ff9900, 0 0 12px #ffaa00;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 153, 0, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(255, 153, 0, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 153, 0, 0); }
    }
    .action-bar {
        display: flex;
        gap: 12px;
        margin-top: 8px;
        font-size: 13px;
        color: #888;
    }
    .action-btn {
        cursor: pointer;
        transition: color 0.2s;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .action-btn:hover {
        color: #ff9900;
    }
    </style>
""", unsafe_allow_html=True)

AI_NAME = "NexusAI"
SYSTEM_PROMPT = f"Your name is {AI_NAME}. You are a smart multi-lingual AI assistant. Respond helpfully and clearly."

# Session Initialization
if "chats" not in st.session_state:
    st.session_state.chats = {"New Chat": []}

if "current_chat_title" not in st.session_state:
    st.session_state.current_chat_title = "New Chat"

# Header
st.title(f"⚡ {AI_NAME}")
st.caption("Your Personal AI Assistant")

# Sidebar
with st.sidebar:
    # NEW CHAT BUTTON
    if st.button("➕ New Chat", use_container_width=True):
        count = len(st.session_state.chats) + 1
        new_title = f"New Chat {count}"
        st.session_state.chats[new_title] = []
        st.session_state.current_chat_title = new_title
        st.rerun()

    st.subheader("📜 Chat History")
    
    titles = list(st.session_state.chats.keys())
    
    def on_chat_change():
        st.session_state.current_chat_title = st.session_state.selected_radio_chat

    st.radio(
        "Select Conversation:",
        options=titles,
        index=titles.index(st.session_state.current_chat_title) if st.session_state.current_chat_title in titles else 0,
        key="selected_radio_chat",
        on_change=on_chat_change
    )

    # Rename chat manually
    new_custom_name = st.text_input("✏️ Rename current chat:", value=st.session_state.current_chat_title)
    if new_custom_name and new_custom_name != st.session_state.current_chat_title:
        st.session_state.chats[new_custom_name] = st.session_state.chats.pop(st.session_state.current_chat_title)
        st.session_state.current_chat_title = new_custom_name
        st.rerun()

    st.divider()
    st.subheader("📁 Upload Files")
    
    uploaded_doc = st.file_uploader("Upload Document (.txt, .pdf)", type=["txt", "pdf"])
    file_context = ""
    if uploaded_doc:
        if uploaded_doc.name.endswith(".txt"):
            file_context = uploaded_doc.read().decode("utf-8")
        elif uploaded_doc.name.endswith(".pdf"):
            pdf_reader = PdfReader(uploaded_doc)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    file_context += text + "\n"
        st.success("Document attached successfully!")

    uploaded_img = st.file_uploader("Upload Image (.png, .jpg)", type=["png", "jpg", "jpeg"])
    img_b64 = None
    if uploaded_img:
        st.image(uploaded_img, caption="Attached Image", use_container_width=True)
        img_bytes = uploaded_img.read()
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')

    st.divider()
    if st.button("🗑️ Clear All History", use_container_width=True):
        st.session_state.chats = {"New Chat": []}
        st.session_state.current_chat_title = "New Chat"
        st.rerun()

# Get current chat messages
current_messages = st.session_state.chats[st.session_state.current_chat_title]

# Render Chat History
for idx, msg in enumerate(current_messages):
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-container"><div class="user-msg">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="chat-container">
                <div class="ai-msg-box">
                    <div class="ai-header">
                        <span class="orange-dot"></span> NexusAI
                    </div>
                    <div>{msg["content"]}</div>
                    <div class="action-bar">
                        <span class="action-btn">📋 Copy</span>
                        <span class="action-btn">👍</span>
                        <span class="action-btn">👎</span>
                        <span class="action-btn">🔗 Share</span>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

# User Chat Input
if prompt := st.chat_input(f"Message {AI_NAME}..."):
    client = Groq(api_key=GROQ_API_KEY)

    # Smart Title Naming
    if len(current_messages) == 0 and ("New Chat" in st.session_state.current_chat_title):
        try:
          title_res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Generate a very short 3-5 word title summarizing the user's topic. Do not use quotes or special characters."},
                    {"role": "user", "content": prompt}
                ]
            )
            generated_title = title_res.choices[0].message.content.strip()

        if img_b64:
            model_name = "llama-3.2-11b-vision-preview"
            content_payload = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
            ]
            messages_payload = [{"role": "user", "content": content_payload}]
        else:
            model_name = "llama-3.1-8b-instant"
            full_sys = SYSTEM_PROMPT + (f"\n\nDocument Context:\n{file_context}" if file_context else "")
            messages_payload = [{"role": "system", "content": full_sys}] + current_messages

        response = client.chat.completions.create(
            model=model_name,
            messages=messages_payload
        )
        reply = response.choices[0].message.content
        current_messages.append({"role": "assistant", "content": reply})
        st.rerun()  
    except Exception as e:
        st.error(f"Error: {e}")