import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

# Hide default Start/Stop buttons
hide_buttons_css = """
    <style>
        button[title="Start"], button[title="Stop"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_buttons_css, unsafe_allow_html=True)

st.title("🚦 Fatigue Detection - Live Stream")

# Simple passthrough video processor (no ML logic yet)
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        return frame  # Just return the original frame

# WebRTC streamer: auto-start, no audio, no storage
webrtc_streamer(
    key="live_video",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    async_processing=True,
    sendback_audio=False
)
