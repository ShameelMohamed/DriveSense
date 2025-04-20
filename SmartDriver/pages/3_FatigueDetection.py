import streamlit as st
import mediapipe as mp
import numpy as np
import pygame
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Constants for fatigue detection
EYE_AR_THRESHOLD = 0.25
YAWN_AR_THRESHOLD = 0.2
HEAD_BEND_THRESHOLD = 20
EYE_AR_CONSEC_FRAMES = 15
MOUTH_OPEN_CONSEC_FRAMES = 7
HEAD_BEND_CONSEC_FRAMES = 10

# Mediapipe initialization
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Function to calculate eye aspect ratio (EAR)
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Function to calculate mouth aspect ratio (MAR)
def mouth_aspect_ratio(mouth):
    A = np.linalg.norm(mouth[13] - mouth[19])
    B = np.linalg.norm(mouth[14] - mouth[18])
    C = np.linalg.norm(mouth[15] - mouth[17])
    D = np.linalg.norm(mouth[12] - mouth[16])
    mar = (A + B + C) / (2.0 * D)
    return mar

# Function to calculate vertical distance between nose tip and eyes
def head_bend_distance(landmarks):
    nose_tip = landmarks[30]
    left_eye = landmarks[36]
    right_eye = landmarks[45]
    eyes_midpoint = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)
    vertical_distance = nose_tip[1] - eyes_midpoint[1]
    return vertical_distance

# Play sound alert
def play_sound(sound_file, volume):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# WebRTC transformer for processing video frames
class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def transform(self, frame):
        # Convert the frame to RGB for mediapipe processing
        frame_rgb = frame.to_rgb()
        results = self.face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                # Extract eye, mouth, and head bend information
                left_eye = []
                right_eye = []
                for i in range(36, 42):
                    left_eye.append(np.array([landmarks.landmark[i].x, landmarks.landmark[i].y]))
                for i in range(42, 48):
                    right_eye.append(np.array([landmarks.landmark[i].x, landmarks.landmark[i].y]))
                mouth = []
                for i in range(48, 68):
                    mouth.append(np.array([landmarks.landmark[i].x, landmarks.landmark[i].y]))

                # Calculate EAR, MAR, and head bend distance
                avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
                mar = mouth_aspect_ratio(mouth)
                vertical_distance = head_bend_distance(landmarks.landmark)

                # Detect fatigue conditions
                if avg_ear < EYE_AR_THRESHOLD:
                    play_sound('alert.wav', 0.5)
                if mar > YAWN_AR_THRESHOLD:
                    play_sound('yawn.wav', 0.5)
                if vertical_distance > HEAD_BEND_THRESHOLD:
                    play_sound('head_bend.wav', 0.5)

        # Return frame to streamlit
        return frame

# Streamlit UI setup
st.title("🚗 Fatigue Detection System")
st.sidebar.header("Alert Settings")
volume = st.sidebar.slider("Volume", 0.0, 1.0, 0.5)

# Run WebRTC video streamer
webrtc_streamer(key="fatigue-detection", video_transformer_factory=VideoTransformer)
