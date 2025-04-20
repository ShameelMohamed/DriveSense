import streamlit as st
import cv2
import numpy as np
import threading
import pygame
import mediapipe as mp
from scipy.spatial import distance

st.set_page_config(page_title="Fatigue Detection", page_icon="🚥", layout="wide", initial_sidebar_state="collapsed")

# Background CSS
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Constants
EYE_AR_THRESHOLD = 0.25
YAWN_AR_THRESHOLD = 0.7
EYE_AR_CONSEC_FRAMES = 15
MOUTH_OPEN_CONSEC_FRAMES = 7

# Initialize mediapipe face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Alert sound function
def play_sound(sound_file, volume):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

# EAR calculation using eye landmarks
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# MAR calculation using mouth landmarks
def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[13], mouth[14])  # Top-lip to bottom-lip
    B = distance.euclidean(mouth[0], mouth[6])    # Width
    return A / B

# App UI
st.title("🚗 Driving Fatigue Management")

with st.sidebar:
    st.header("Alert Settings")
    volume = st.slider("Volume", 0.0, 1.0, 0.5)
    st.session_state.eye_alert = st.checkbox("Detect Eyes Closure", value=st.session_state.get("eye_alert", False))
    st.session_state.yawn_alert = st.checkbox("Detect Yawning", value=st.session_state.get("yawn_alert", False))
    st.session_state.all_alert = st.checkbox("Detect All", value=True)
    sound_option = st.radio("Select Alert Sound", ["beep", "buzzer", "horn"])

if "running" not in st.session_state:
    st.session_state.running = False

def detect_fatigue():
    cap = cv2.VideoCapture(0)
    eye_counter = 0
    mouth_counter = 0
    frame_window = st.empty()

    while st.session_state.running:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not available.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        alert_text = ""
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Extract relevant eye and mouth landmarks
                landmarks = face_landmarks.landmark
                h, w, _ = frame.shape

                left_eye_idx = [362, 385, 387, 263, 373, 380]
                right_eye_idx = [33, 160, 158, 133, 153, 144]
                mouth_idx = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415, 310, 311]

                left_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in left_eye_idx]
                right_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in right_eye_idx]
                mouth = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in mouth_idx]

                # EAR and MAR
                ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
                mar = mouth_aspect_ratio(mouth)

                color = (0, 255, 0)

                # Eye alert
                if (st.session_state.eye_alert or st.session_state.all_alert) and ear < EYE_AR_THRESHOLD:
                    eye_counter += 1
                    if eye_counter >= EYE_AR_CONSEC_FRAMES:
                        threading.Thread(target=play_sound, args=(f"{sound_option}.wav", volume), daemon=True).start()
                        alert_text = "Eyes Closed!"
                        color = (0, 0, 255)
                        eye_counter = 0
                else:
                    eye_counter = 0

                # Yawn alert
                if (st.session_state.yawn_alert or st.session_state.all_alert) and mar > YAWN_AR_THRESHOLD:
                    mouth_counter += 1
                    if mouth_counter >= MOUTH_OPEN_CONSEC_FRAMES:
                        threading.Thread(target=play_sound, args=(f"{sound_option}.wav", volume), daemon=True).start()
                        alert_text = "Yawning!"
                        color = (0, 0, 255)
                        mouth_counter = 0
                else:
                    mouth_counter = 0

                cv2.putText(frame, alert_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        frame_window.image(frame, channels="BGR", use_column_width=True)
    cap.release()
    st.write("Fatigue detection stopped.")

# Start / Stop Button
if st.button("Start / Stop"):
    if not st.session_state.running:
        st.session_state.running = True
        detect_fatigue()
    else:
        st.session_state.running = False
