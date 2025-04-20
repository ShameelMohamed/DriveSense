import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.set_page_config(page_title="Live Video", layout="wide")
st.title("🎥 Live Webcam Stream")

# Hide Streamlit WebRTC control buttons using CSS
st.markdown("""
    <style>
    button[title="Start"], button[title="Stop"], button[title="Snapshot"] {
        visibility: hidden !important;
        height: 0px !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Dummy video processor to stream frames (no logic)
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        return frame

# Auto-start video stream
webrtc_streamer(
    key="auto_stream",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    async_processing=True
)
