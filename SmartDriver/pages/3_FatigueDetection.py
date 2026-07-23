import streamlit as st
import cv2
import dlib
from scipy.spatial import distance
import numpy as np
import threading
import os
import urllib.request
import bz2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

st.set_page_config(page_title="Fatigue Detection", page_icon="🚥", layout="wide", initial_sidebar_state="collapsed")

background_css = """
<style>
    /* Background Image */
    .stApp {
        background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Hide default Streamlit header */
    header {
        visibility: hidden;
    }
</style>
"""

# Inject the CSS into the page
st.markdown(background_css, unsafe_allow_html=True)

# Constants
EYE_AR_THRESHOLD = 0.25  # Adjusted threshold for eye aspect ratio
YAWN_AR_THRESHOLD = 0.2
HEAD_BEND_THRESHOLD = 20
EYE_AR_CONSEC_FRAMES = 15
MOUTH_OPEN_CONSEC_FRAMES = 7
HEAD_BEND_CONSEC_FRAMES = 10

# Load dlib's face detector and facial landmark predictor
@st.cache_resource
def load_dlib_models():
    model_path = "shape_predictor_68_face_landmarks.dat"
    if not os.path.exists(model_path):
        url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
        st.info("Downloading face landmark model (this may take a moment)...")
        urllib.request.urlretrieve(url, model_path + ".bz2")
        with bz2.BZ2File(model_path + ".bz2") as fr, open(model_path, "wb") as fw:
            fw.write(fr.read())
        os.remove(model_path + ".bz2")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model_path)
    return detector, predictor

detector, predictor = load_dlib_models()

# Function to calculate eye aspect ratio (EAR)
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Function to calculate mouth aspect ratio (MAR)
def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[13], mouth[19])
    B = distance.euclidean(mouth[14], mouth[18])
    C = distance.euclidean(mouth[15], mouth[17])
    D = distance.euclidean(mouth[12], mouth[16])
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

# Streamlit app
st.title("🚗 Driving Fatigue Management")
st.title("")

# Sidebar elements
with st.sidebar:
    st.header("Alert Settings")
    eye_alert = st.checkbox("Detect Eyes Closure", value=True)
    head_alert = st.checkbox("Detect Head Down", value=True)
    yawn_alert = st.checkbox("Detect Yawning", value=True)
    all_alert = st.checkbox("Detect All", value=True)
    st.info("Ensure you grant camera permissions to use the fatigue detector.")

class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.eye_counter = 0
        self.mouth_open_counter = 0
        self.head_bend_counter = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = np.array([[p.x, p.y] for p in landmarks.parts()])
            left_eye, right_eye = landmarks[42:48], landmarks[36:42]
            mouth = landmarks[48:68]

            # Calculate the eye aspect ratio
            avg_ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0
            mar = mouth_aspect_ratio(mouth)
            vertical_distance = head_bend_distance(landmarks)

            color = (0, 255, 0)
            alert_text = ""

            # Detect Eyes Closure
            if (eye_alert or all_alert) and avg_ear < EYE_AR_THRESHOLD:
                self.eye_counter += 1
                if self.eye_counter >= EYE_AR_CONSEC_FRAMES:
                    alert_text = "Eyes Closed!"
                    color = (0, 0, 255)
            else:
                self.eye_counter = 0

            # Detect Yawning
            if (yawn_alert or all_alert) and mar > YAWN_AR_THRESHOLD:
                self.mouth_open_counter += 1
                if self.mouth_open_counter >= MOUTH_OPEN_CONSEC_FRAMES:
                    alert_text = "Yawning Detected!"
                    color = (0, 0, 255)
            else:
                self.mouth_open_counter = 0

            # Detect Head Down
            if (head_alert or all_alert) and vertical_distance > HEAD_BEND_THRESHOLD:
                self.head_bend_counter += 1
                if self.head_bend_counter >= HEAD_BEND_CONSEC_FRAMES:
                    alert_text = "Head Down!"
                    color = (0, 0, 255)
            else:
                self.head_bend_counter = 0

            cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()), color, 2)
            if alert_text:
                cv2.putText(img, alert_text, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

webrtc_streamer(
    key="fatigue-detection",
    video_processor_factory=VideoProcessor,
    rtc_configuration=rtc_configuration,
    media_stream_constraints={"video": True, "audio": False},
)

