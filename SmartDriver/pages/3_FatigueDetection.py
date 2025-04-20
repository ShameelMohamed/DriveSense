import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.set_page_config(page_title="Live Video", layout="wide")
st.title("🎥 Live Webcam Stream")

# CSS to hide buttons and container spacing
st.markdown("""
    <style>
    .MuiButtonBase-root {
        display: none !important;
    }
    [data-testid="stVideoStream"] button {
        display: none !important;
    }
    .MuiBox-root {
        padding: 0 !important;
        margin: 0 !important;
        height: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Dummy processor
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        return frame

# Stream without buttons
webrtc_streamer(
    key="stream",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    async_processing=True
)
