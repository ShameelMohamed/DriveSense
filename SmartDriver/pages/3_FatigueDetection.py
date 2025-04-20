import streamlit as st
import streamlit_webrtc as webrtc

# Streamlit page configuration
st.set_page_config(page_title="Live Video Capture", layout="wide")

# Add title
st.title("Live Video Capture with Streamlit")

# WebRTC configuration for capturing video
class VideoProcessor:
    def recv(self, frame):
        return frame  # Just return the frame for now

# Create a WebRTC component to capture live video
webrtc_streamer = webrtc.StreamlitWebRtc(
    key="live-video-capture", 
    video_processor_factory=VideoProcessor, 
    media_stream_constraints={"video": True}
)

# Display message for users
if webrtc_streamer.video_transformer:
    st.write("Video stream is running...")
else:
    st.write("Waiting for video stream...")
