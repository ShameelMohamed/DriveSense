import streamlit as st
import numpy as np
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import math
import pygame
import threading

st.set_page_config(page_title="Fatigue Detection", page_icon="😴", layout="wide")

# Pygame sound init
def play_alert(volume):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load("beep.wav")  # Make sure beep.wav is in same folder
    pygame.mixer.music.play()

# EAR calculator
def eye_aspect_ratio(landmarks, eye_indices):
    p = [np.array([landmarks[i][0], landmarks[i][1]]) for i in eye_indices]
    A = np.linalg.norm(p[1] - p[5])
    B = np.linalg.norm(p[2] - p[4])
    C = np.linalg.norm(p[0] - p[3])
    ear = (A + B) / (2.0 * C)
    return ear

# MAR calculator
def mouth_aspect_ratio(landmarks):
    top = np.array(landmarks[13])
    bottom = np.array(landmarks[14])
    mar = np.linalg.norm(top - bottom)
    return mar

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.EYE_AR_THRESH = 0.23
        self.EYE_AR_CONSEC_FRAMES = 15
        self.MOUTH_AR_THRESH = 15  # Pixel distance
        self.MOUTH_AR_FRAMES = 7
        self.eye_counter = 0
        self.mouth_counter = 0

    def transform(self, frame):
        rgb_frame = frame.to_ndarray(format="bgr24")
        img_rgb = rgb_frame[:, :, ::-1]

        results = self.face_mesh.process(img_rgb)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            h, w, _ = img_rgb.shape
            coords = [(int(p.x * w), int(p.y * h)) for p in landmarks.landmark]

            # Eye landmark indices (mediapipe face mesh)
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]

            left_ear = eye_aspect_ratio(coords, LEFT_EYE)
            right_ear = eye_aspect_ratio(coords, RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2

            mar = mouth_aspect_ratio(coords)

            if avg_ear < self.EYE_AR_THRESH:
                self.eye_counter += 1
                if self.eye_counter >= self.EYE_AR_CONSEC_FRAMES:
                    threading.Thread(target=play_alert, args=(volume,), daemon=True).start()
                    cv2.putText(rgb_frame, "Eyes Closed!", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                self.eye_counter = 0

            if mar > self.MOUTH_AR_THRESH:
                self.mouth_counter += 1
                if self.mouth_counter >= self.MOUTH_AR_FRAMES:
                    threading.Thread(target=play_alert, args=(volume,), daemon=True).start()
                    cv2.putText(rgb_frame, "Yawning!", (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                self.mouth_counter = 0

        return rgb_frame

# Sidebar settings
st.sidebar.title("Settings")
volume = st.sidebar.slider("Volume", 0.0, 1.0, 0.5)

st.title("😴 Real-Time Fatigue Detection")
st.markdown("Detects **eye closure** and **yawning** using Mediapipe and WebRTC. No OpenCV or dlib used.")

# Start webcam
webrtc_streamer(key="fatigue", video_transformer_factory=VideoTransformer)
