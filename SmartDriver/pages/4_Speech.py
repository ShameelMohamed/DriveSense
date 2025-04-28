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

# --- Background & Styling ---
background_css = """
<style>
    .stApp {
        background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    header, footer {visibility: hidden;}

    /* FULL-WIDTH MICROPHONE BUTTON SOLUTION */
    .mic-container {
        position: relative;
        width: 100vw;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
    }

    .mic-container > div {
        width: 100% !important;
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
        background: transparent !important;
    }

    .mic-container button {
        width: 100% !important;
        background: #ff4b4b !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 20px !important;
        padding: 16px 32px !important;
        border: 2px solid white !important;
        border-radius: 16px !important;
        box-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b !important;
        animation: glow 2s infinite alternate !important;
        transition: 0.3s ease !important;
    }

    .mic-container button:hover {
        background-color: #ff7b7b !important;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b; }
        to { box-shadow: 0 0 20px #ff7b7b, 0 0 40px #ff7b7b; }
    }
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# --- API Configuration ---
aai.settings.api_key = ASSEMBLYAI_API_KEY
gen_ai.configure(api_key=GEMINI_API_KEY)

# Voice IDs
ELEVENLABS_VOICE_ID_MALE = "pNInz6obpgDQGcFmaJgB"
ELEVENLABS_VOICE_ID_FEMALE = "21m00Tcm4TlvDq8ikWAM"

# --- App Title ---
st.title("🤖 Ask Pookie - Your AI Companion")

# --- Sidebar Settings ---
st.sidebar.header("Settings")
voice_selection = st.sidebar.radio("Select Voice", ["Male", "Female"])
language_selection = st.sidebar.radio("Choose Language", ["English", "Tamil", "Malayalam", "Telugu", "Hindi"], index=0)
volume_percent = st.sidebar.slider("Volume", 0, 100, 100)

# --- Voice ID ---
ELEVENLABS_VOICE_ID = ELEVENLABS_VOICE_ID_FEMALE if voice_selection == "Female" else ELEVENLABS_VOICE_ID_MALE
ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

# --- Functions ---

def transcribe_audio(audio_file):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    return transcript.text if transcript else ""

def gemini_chat(query, lang):
    try:
        prompt = f"Respond in {lang}. For the query '{query}', generate a helpful response in 10-25 words without asking follow-up questions."
        model = gen_ai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def text_to_speech_elevenlabs(text):
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY,
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }
    response = requests.post(ELEVENLABS_URL, json=data, headers=headers)

    if response.status_code == 200:
        audio_path = "response_audio.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        return audio_path
    else:
        st.error(f"⚠ ElevenLabs API Error: {response.text}")
        return None

# --- Main App ---

st.subheader("🎙 Record your voice")

# Mic Recorder - Now truly full-width
st.markdown('<div class="mic-container">', unsafe_allow_html=True)
audio_data = mic_recorder(
    start_prompt="🎤 Start recording",
    stop_prompt="⏹ Stop recording",
    key="recorder"
)
st.markdown('</div>', unsafe_allow_html=True)

# After Recording
if audio_data:
    st.success("✅ Recording complete!")

    audio_bytes = audio_data["bytes"]

    st.audio(audio_bytes, format="audio/wav")

    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)

    user_text = transcribe_audio("temp_audio.wav")

    if user_text.strip():
        st.success(f"✅ Recognized: {user_text}")
        response = gemini_chat(user_text, language_selection)

        st.subheader("💬 AI Response")
        st.write(response)

        audio_path = text_to_speech_elevenlabs(response)
        if audio_path:
            st.audio(audio_path, format="audio/mp3")
            st.info(f"🔊 Set your system volume to {volume_percent}% for best experience.")
        else:
            st.error("⚠ Failed to generate speech.")
    else:
        st.warning("❌ No speech detected, please try again.")
else:
    st.info("⬆ Click the mic button above to record!")
