import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import threading
import pygame
import math

# UI Setup
st.set_page_config(page_title="Fatigue Detection", layout="wide")

st.title("😴 Fatigue Detection using MediaPipe")

# Sidebar controls
with st.sidebar:
    st.header("Alert Settings")
    volume = st.slider("Volume", 0.0, 1.0, 0.5)
    eye_alert = st.checkbox("Detect Eye Closure", value=True)
    yawn_alert = st.checkbox("Detect Yawning", value=True)
    head_alert = st.checkbox("Detect Head Down", value=True)
    sound_option = st.radio("Alert Sound", ["beep", "buzzer", "horn"])

# Sound alert function
def play_alert(sound_file, volume):
    try:
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except:
        pass

# EAR calculation
def eye_aspect_ratio(landmarks, eye_indices):
    p1 = np.array(landmarks[eye_indices[1]])
    p2 = np.array(landmarks[eye_indices[5]])
    p3 = np.array(landmarks[eye_indices[2]])
    p4 = np.array(landmarks[eye_indices[4]])
    p5 = np.array(landmarks[eye_indices[0]])
    p6 = np.array(landmarks[eye_indices[3]])

    A = np.linalg.norm(p2 - p4)
    B = np.linalg.norm(p3 - p5)
    C = np.linalg.norm(p1 - p6)

    ear = (A + B) / (2.0 * C)
    return ear

# Main detection loop
def fatigue_detection():
    cap = cv2.VideoCapture(0)
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    MOUTH = [13, 14]

    EYE_AR_THRESH = 0.25
    YAWN_THRESH = 25  # Distance between lips
    HEAD_BEND_THRESH = 15

    eye_counter = 0
    yawn_counter = 0
    head_counter = 0

    eye_limit = 15
    yawn_limit = 7
    head_limit = 10

    frame_window = st.empty()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.error("Camera not found.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        frame_h, frame_w = frame.shape[:2]
        alert = ""

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = [(int(lm.x * frame_w), int(lm.y * frame_h)) for lm in face_landmarks.landmark]

                # EAR
                left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
                right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
                avg_ear = (left_ear + right_ear) / 2.0

                # Eye alert
                if eye_alert and avg_ear < EYE_AR_THRESH:
                    eye_counter += 1
                    if eye_counter > eye_limit:
                        alert = "Eyes Closed!"
                        threading.Thread(target=play_alert, args=(f"{sound_option}.wav", volume), daemon=True).start()
                        eye_counter = 0
                else:
                    eye_counter = 0

                # Yawning detection
                if yawn_alert:
                    mouth_top = landmarks[MOUTH[0]]
                    mouth_bottom = landmarks[MOUTH[1]]
                    mouth_dist = abs(mouth_top[1] - mouth_bottom[1])
                    if mouth_dist > YAWN_THRESH:
                        yawn_counter += 1
                        if yawn_counter > yawn_limit:
                            alert = "Yawning!"
                            threading.Thread(target=play_alert, args=(f"{sound_option}.wav", volume), daemon=True).start()
                            yawn_counter = 0
                    else:
                        yawn_counter = 0

                # Head down detection (nose vs eyes)
                if head_alert:
                    nose_y = landmarks[1][1]
                    eye_y = (landmarks[33][1] + landmarks[263][1]) // 2
                    head_dist = nose_y - eye_y
                    if head_dist > HEAD_BEND_THRESH:
                        head_counter += 1
                        if head_counter > head_limit:
                            alert = "Head Down!"
                            threading.Thread(target=play_alert, args=(f"{sound_option}.wav", volume), daemon=True).start()
                            head_counter = 0
                    else:
                        head_counter = 0

                # Draw alert
                if alert:
                    cv2.putText(frame, alert, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        frame_window.image(frame, channels="BGR", use_column_width=True)

    cap.release()

# Start button
if st.button("Start Detection"):
    fatigue_detection()
