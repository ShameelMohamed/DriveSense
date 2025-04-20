import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import requests
import numpy as np
import io

# Function to detect face landmarks using Face++
def detect_face_landmarks(image):
    api_key = '_B8RMNDG79kuycugJsE_YzX6fwn1n6ws'
    api_secret = 'svGox2wtFa95Lqn9aDuujjg6DEGnQJl5'
    
    url = "https://api-us.faceplusplus.com/facepp/v3/detect"
    files = {'image_file': image}  # image is the image file to send
    data = {
        'api_key': api_key,
        'api_secret': api_secret,
        'return_landmark': 1  # Request landmarks
    }
    
    response = requests.post(url, data=data, files=files)
    return response.json()

# Dummy fatigue detection (replace with your actual logic)
def is_fatigued(landmarks):
    # Implement fatigue detection logic based on landmarks here
    return False  # Dummy return value for now

# VideoProcessor for webrtc_streamer
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        # Convert the frame to image format for API
        image_bytes = frame.to_image().tobytes()
        image_file = io.BytesIO(image_bytes)

        # Detect face landmarks using the API
        response = detect_face_landmarks(image_file)
        landmarks = response.get('faces', [])[0].get('landmark', {}) if response.get('faces') else {}

        # Fatigue detection logic (dummy for now)
        if is_fatigued(landmarks):
            st.warning("Fatigue detected!")

        # Return the frame (optionally, you can modify the frame here)
        return frame

# Stream without buttons
webrtc_streamer(
    key="stream",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    async_processing=True
)
