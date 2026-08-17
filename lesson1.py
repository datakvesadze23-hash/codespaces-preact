import streamlit as st
import base64
from groq import Groq
from pypdf import PdfReader
from io import BytesIO

# Page Setup - Using Velox AI Assistant
st.set_page_config(page_title="Velox AI Assistant", page_icon="⚡", layout="wide")

# API KEY from secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# Custom Styling for chat messages
st.markdown("""
    <style>
    .chat-container { display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }
    .user-msg { align-self: flex-end; background-color: #f0f2f6; color: #000000; padding: 12px 18px; border-radius: 18px 18px 2px 18px; max-width: 70%; }
    .bot-msg { align-self: flex-start; background-color: #e8f0fe; color: #000000; padding: 12px 18px; border-radius: 18px 18px 18px 2px; max-width: 70%; }
    .stApp > header { display: none !important; } /* Hide only top Streamlit header */
    </style>
""", unsafe_allow_html=True)

# Main Title
st.title("⚡ Velox AI Assistant")

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

# --- SIDEBAR (The Left Side) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/datakvesadze23-hash/codespaces-preact/main/logo.png", width=150) # You can upload your own logo to GitHub and put the link here
    st.title("Velox Control Panel")
    st.markdown("გამარჯობა! მე ვარ **Velox AI**, შენი სწრაფი და ჭკვიანი ასისტენტი.")
    st.divider()
    
    # PDF Upload Functionality
    uploaded_file = st.file_uploader("ატვირთე PDF დოკუმენტი კონტექსტისთვის", type="pdf")
    
    if uploaded_file is not None:
        try:
            reader = PdfReader(BytesIO(uploaded_file.read()))
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()
            st.session_state.pdf_context = pdf_text
            st.success("✅ PDF წარმატებით დამუშავდა!")
        except Exception as e:
            st.error(f"❌ PDF-ის წაკითხვისას მოხდა შეცდომა: {e}")
            st.session_state.pdf_context = ""
    else:
        st.session_state.pdf_context = ""

    st.divider()
    if st.button("ჩატის გასუფთავება"):
        st.session_state.messages = []
        st.session_state.pdf_context = ""
        st.rerun()

# --- MAIN CHAT AREA ---

# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Copy button for bot response
        if message["role"] == "assistant":
            escaped_text = message["content"].replace("`", "\\`").replace('"', '\\"')
            copy_code = f"""
            <button onclick="navigator.clipboard.writeText(`{escaped_text}`);" 
                    style="background: transparent; border: 1px solid #ccc; border-radius: 6px; padding: 4px 10px; cursor: pointer; color: black; font-size: 14px;">
                📋 Copy
            </button>
            """
            st.components.v1.html(copy_code, height=45)

# Chat Input
if prompt := st.chat_input("ჩაწერე შეკითხვა..."):
    # Build full prompt with PDF context if available
    full_prompt = prompt
    if st.session_state.pdf_context:
        full_prompt = f"--- PDF კონტექსტი ---\n{st.session_state.pdf_context}\n----------------------\n\nმომხმარებლის შეკითხვა: {prompt}"

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Velox AI, a smart assistant. Use the provided PDF context if it exists."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": full_prompt} # Send full prompt with context, but only 'prompt' in history
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()