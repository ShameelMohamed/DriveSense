# --- API Keys ---
ASSEMBLYAI_API_KEY = "11c6274223b9472fa206d42b02f1de1f"
GEMINI_API_KEY = "AIzaSyByJzlUoKiO1y1xytWczcnQvda9SAwYReo"
ELEVENLABS_API_KEY = "sk_a16a7b74f453342e927cbecec40312123880e614972b9563"

import streamlit as st
import assemblyai as aai
import google.generativeai as gen_ai
import requests
from streamlit_mic_recorder import mic_recorder

# --- Streamlit Page Settings ---
st.set_page_config(
    page_title="AI Voice Companion",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FULL-WIDTH MICROPHONE BUTTON SOLUTION ---
st.markdown("""
<style>
    /* NUCLEAR OPTION - OVERRIDE ALL CONTAINERS */
    div[data-testid="stAppViewBlockContainer"] > div:first-child {
        max-width: none !important;
        padding: 0 !important;
    }
    
    /* TARGET THE BUTTON DIRECTLY */
    div.stButton > button {
        width: 100vw !important;
        position: relative !important;
        left: 50% !important;
        right: 50% !important;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        border-radius: 0 !important;
        display: block !important;
    }
    
    /* MIC BUTTON STYLING */
    div.stButton > button {
        background: #ff4b4b !important;
        color: white !important;
        font-size: 24px !important;
        padding: 24px !important;
        border: none !important;
        box-shadow: 0 0 30px #ff4b4b !important;
        transition: all 0.3s !important;
    }
    
    div.stButton > button:hover {
        background: #ff6b6b !important;
        box-shadow: 0 0 50px #ff6b6b !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Rest of your existing code ---
aai.settings.api_key = ASSEMBLYAI_API_KEY
gen_ai.configure(api_key=GEMINI_API_KEY)

# Voice IDs
ELEVENLABS_VOICE_ID_MALE = "pNInz6obpgDQGcFmaJgB"
ELEVENLABS_VOICE_ID_FEMALE = "21m00Tcm4TlvDq8ikWAM"

# App Title
st.title("🤖 Ask Pookie - Your AI Companion")

# Sidebar Settings
with st.sidebar:
    st.header("Settings")
    voice_selection = st.radio("Select Voice", ["Male", "Female"])
    language_selection = st.radio("Choose Language", ["English", "Tamil", "Malayalam", "Telugu", "Hindi"])
    volume_percent = st.slider("Volume", 0, 100, 100)

# Voice Selection
ELEVENLABS_VOICE_ID = ELEVENLABS_VOICE_ID_FEMALE if voice_selection == "Female" else ELEVENLABS_VOICE_ID_MALE
ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

# --- Functions (keep your existing functions) ---
def transcribe_audio(audio_file): ...
def gemini_chat(query, lang): ...
def text_to_speech_elevenlabs(text): ...

# --- FULL-WIDTH MICROPHONE IMPLEMENTATION ---
st.subheader("🎙 Record your voice")

# This button will now span the ENTIRE viewport width
audio_data = mic_recorder(
    start_prompt="🎤 SPEAK NOW (Full Screen Width)",
    stop_prompt="⏹ STOP RECORDING",
    key="fullwidth_recorder"
)

# Rest of your recording handling logic...
if audio_data:
    st.success("✅ Recording complete!")
    audio_bytes = audio_data["bytes"]
    st.audio(audio_bytes, format="audio/wav")
    
    # ... rest of your processing logic
else:
    st.info("⬆ Click the microphone button to start recording")
