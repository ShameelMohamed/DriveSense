import streamlit as st
from streamlit_audio_recorder import audio_recorder
import assemblyai as aai
import google.generativeai as gen_ai
import requests
import os

st.set_page_config(page_title="AI Voice Assistant", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

background_css = """
<style>
    .stApp {
        background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    header { visibility: hidden; }
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# API keys
aai.settings.api_key = "your-assemblyai-api-key"
gen_ai.configure(api_key="your-gemini-api-key")

model = gen_ai.GenerativeModel('gemini-1.5-flash')

ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
ELEVENLABS_VOICE_ID_MALE = "pNInz6obpgDQGcFmaJgB"
ELEVENLABS_VOICE_ID_FEMALE = "21m00Tcm4TlvDq8ikWAM"

# Sidebar
st.sidebar.header("Settings")
voice = st.sidebar.radio("Select Voice", ["Male", "Female"])
voice_id = ELEVENLABS_VOICE_ID_FEMALE if voice == "Female" else ELEVENLABS_VOICE_ID_MALE
ELEVENLABS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# Title
st.title("🤖 Ask Pookie - Your AI Assistant")

# Record using audio_recorder
wav_audio = audio_recorder(pause_threshold=2.0)

if wav_audio:
    audio_file_path = "temp_audio.wav"
    with open(audio_file_path, "wb") as f:
        f.write(wav_audio)

    st.success("Recording captured!")

    # Transcribe
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)
    user_input = transcript.text

    if user_input:
        st.write("You said:", user_input)

        # Gemini AI response
        response = model.generate_content(
            f"For the query '{user_input}' generate content in 10-25 words. Do not ask questions back."
        )
        bot_reply = response.text
        st.subheader("Pookie says:")
        st.write(bot_reply)

        # Text-to-Speech
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY,
        }
        data = {
            "text": bot_reply,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }

        res = requests.post(ELEVENLABS_URL, json=data, headers=headers)
        if res.status_code == 200:
            with open("reply.mp3", "wb") as f:
                f.write(res.content)
            st.audio("reply.mp3", format="audio/mp3")
        else:
            st.error("Failed to generate speech.")
