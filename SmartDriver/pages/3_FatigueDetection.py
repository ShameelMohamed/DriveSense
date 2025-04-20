import streamlit as st
import streamlit_webrtc as webrtc
from streamlit_webrtc import VideoTransformerBase

# Streamlit page configuration
st.set_page_config(page_title="Live Video Capture", layout="wide")

# Add title
st.title("Live Video Capture with Streamlit")

# Video Transformer class to handle the video frame processing
class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        return frame  # Just return the frame without modifications for now

# WebRTC configuration for capturing and displaying video
webrtc_streamer = webrtc.webrtc_streamer(
    key="live-video-capture", 
    video_transformer_factory=VideoTransformer, 
    media_stream_constraints={"video": True}
)

# Display message for users
if webrtc_streamer.video_transformer:
    st.write("Video stream is running...")
else:
    st.write("Waiting for video stream...")
