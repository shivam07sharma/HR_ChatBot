import streamlit as st
import requests
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Holographic Chat",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS (Original Style + Scrollbar Fix + Card Fix) ---
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&display=swap');

* {
    font-family: 'Space Grotesk', sans-serif !important;
    box-sizing: border-box !important;
}

/* Prevent unwanted horizontal/vertical scrollbars on mobile */
html, body, [data-testid="stAppViewContainer"] {
    overflow-x: hidden !important;
    background-color: #0F172A;
}

/* Deep Space Theme */
.stApp {
    background-color: #0F172A;
    background-image: 
        radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 85% 90%, rgba(168, 85, 247, 0.15) 0%, transparent 40%);
    background-attachment: fixed;
    color: #F8FAFC;
}

header, footer, [data-testid="collapsedControl"] {
    visibility: hidden !important;
    display: none !important;
}

/* Glass Login Card */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(30, 41, 59, 0.35) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    padding: 2.5rem 2rem !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 
                0 0 15px rgba(99, 102, 241, 0.15) inset !important;
    margin-top: 14vh !important;
}

/* Inputs */
.stTextInput > div > div > input {
    background: rgba(15, 23, 42, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #818CF8 !important;
    box-shadow: 0 0 15px rgba(129, 140, 248, 0.3) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    box-shadow: 0 0 20px rgba(168, 85, 247, 0.6) !important;
    transform: translateY(-1px) !important;
}

/* Chat Topbar */
.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

/* Custom Chat Bubbles */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin-bottom: 20px !important;
}

/* AI Message */
[data-testid="stChatMessage"]:has([aria-label="assistant"]) > div:last-child {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 0 18px 18px 18px;
    padding: 14px 18px;
    max-width: 82%;
}

/* User Message */
[data-testid="stChatMessage"]:has([aria-label="user"]) {
    flex-direction: row-reverse !important;
}
[data-testid="stChatMessage"]:has([aria-label="user"]) > div:last-child {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.8) 0%, rgba(168, 85, 247, 0.8) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px 0 18px 18px;
    padding: 14px 18px;
    max-width: 82%;
    margin-left: auto;
}
[data-testid="stChatMessage"]:has([aria-label="user"]) [data-testid="chatAvatarIcon-user"] {
    margin-left: 1rem !important;
    margin-right: 0 !important;
}

/* Bottom Input */
[data-testid="stChatInput"] {
    background: rgba(30, 41, 59, 0.7) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    margin-bottom: 15px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
}
[data-testid="stChatInput"] textarea {
    color: white !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# --- SVG Avatars ---
USER_SVG = "data:image/svg+xml;base64," + base64.b64encode(b"""
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="24" height="24" rx="12" fill="#6366F1" fill-opacity="0.2"/>
<circle cx="12" cy="8" r="3.5" stroke="#818CF8" stroke-width="1.8"/>
<path d="M6 19C6 16.5 8.5 14.5 12 14.5C15.5 14.5 18 16.5 18 19" stroke="#818CF8" stroke-width="1.8" stroke-linecap="round"/>
</svg>
""").decode("utf-8")

AI_SVG = "data:image/svg+xml;base64," + base64.b64encode(b"""
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="24" height="24" rx="12" fill="#A855F7" fill-opacity="0.2"/>
<path d="M12 2L14.4 8.4L21 9L15.6 13.2L17.4 19.8L12 16.2L6.6 19.8L8.4 13.2L3 9L9.6 8.4L12 2Z" fill="#D8B4FE" stroke="#C084FC" stroke-width="1.5" stroke-linejoin="round"/>
</svg>
""").decode("utf-8")

# --- Backend Integration ---
API_URL = "http://localhost:8000"

def api_chat(user_id: str, message: str) -> str:
    try:
        response = requests.post(f"{API_URL}/chat", json={"user_id": user_id, "message": message}, timeout=12)
        if response.status_code == 200:
            return response.json().get("response", "No response text found.")
        return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Backend unreachable: {e}"

def api_get_history(user_id: str):
    """Purani conversations load karne ka function"""
    try:
        response = requests.get(f"{API_URL}/history", params={"user_id": user_id}, timeout=6)
        if response.status_code == 200:
            return response.json().get("messages", [])
    except Exception:
        pass
    return []

def api_logout(user_id: str):
    try:
        requests.post(f"{API_URL}/logout", json={"user_id": user_id}, timeout=5)
    except Exception:
        pass

# --- State Management ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Views ---
def view_login():
    _, col_card, _ = st.columns([1, 1.8, 1])
    
    with col_card:
        # Streamlit ka built-in border container (sara content ab box ke andar aayega)
        with st.container(border=True):
            st.markdown(
                "<h2 style='text-align: center; margin-bottom: 1.8rem; background: linear-gradient(to right, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>SYSTEM_ACCESS</h2>", 
                unsafe_allow_html=True
            )
            
            user_id = st.text_input("IDENTIFIER", placeholder="e.g. shivam", label_visibility="collapsed")
            
            if st.button("INITIALIZE SECURE UPLINK", use_container_width=True):
                clean_id = user_id.strip().lower()
                if clean_id:
                    st.session_state.user_id = clean_id
                    st.session_state.logged_in = True
                    
                    # History fetch call
                    with st.spinner("Restoring past conversation..."):
                        history_data = api_get_history(clean_id)
                        st.session_state.messages = history_data
                    st.rerun()
                else:
                    st.warning("Identifier required.")

def view_chat():
    # Chat Header
    c_title, c_btn = st.columns([4, 1])
    with c_title:
        st.markdown(f"<div style='font-weight: 600; color: #818CF8; padding-top: 6px; letter-spacing: 1px;'>ID :: {st.session_state.user_id.upper()}</div>", unsafe_allow_html=True)
    with c_btn:
        if st.button("DISCONNECT", use_container_width=True):
            api_logout(st.session_state.user_id)
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.session_state.user_id = ""
            st.rerun()

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Render Messages
    for msg in st.session_state.messages:
        avatar = USER_SVG if msg["role"] == "user" else AI_SVG
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Transmit message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=USER_SVG):
            st.markdown(prompt)
            
        with st.chat_message("assistant", avatar=AI_SVG):
            with st.spinner("Processing context..."):
                response_text = api_chat(st.session_state.user_id, prompt)
            st.markdown(response_text)
            
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# --- Router ---
if not st.session_state.logged_in:
    view_login()
else:
    view_chat()