import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time

# Set up the Streamlit page
st.set_page_config(page_title="Live Video Feed", layout="wide")

# Video display window
st.title("🚗 Live Video Feed for Fatigue Detection")

# Placeholder for video feed
frame_placeholder = st.empty()

# Define video transformer for streamlit_webrtc (or custom WebRTC handler)
class VideoTransformer:
    def __init__(self):
        self.prev_frame_time = 0

    def transform(self, frame):
        # Convert the frame to a numpy array in RGB format
        image = frame.to_ndarray(format="rgb24")

        # Optionally, you can add any processing here (such as fatigue detection)
        # Example: If you want to display something on the frame, like text

        current_time = time.time()
        fps = 1 / (current_time - self.prev_frame_time)
        self.prev_frame_time = current_time

        # Display FPS on the frame
        st.text(f"FPS: {int(fps)}")

        # Show the video in Streamlit
        frame_placeholder.image(image)

        return frame

# Initialize WebRTC for live streaming
webrtc_streamer = webrtc_streamer(
    key="live-video-capture",  # Unique key for Streamlit session state
    mode=WebRtcMode.SENDRECV,  # Receive and send video
    video_processor_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False}  # Only video
)

