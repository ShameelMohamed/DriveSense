import streamlit as st
from transformers import pipeline
import pygame
from PIL import Image
import numpy as np

# Initialize Streamlit's page configuration
st.set_page_config(page_title="Fatigue Detection", page_icon="🚗", layout="wide", initial_sidebar_state="collapsed")

# Initialize the Hugging Face model for classification (you can replace it with a custom fatigue model)
fatigue_model = pipeline("image-classification", model="your-hugging-face-model")

# Initialize pygame for alert sound
def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Streamlit Sidebar for alert settings
with st.sidebar:
    st.header("Alert Settings")
    volume = st.slider("Volume", 0.0, 1.0, 0.5)
    st.session_state.eye_alert = st.checkbox("Detect Eyes Closure", value=True)
    st.session_state.head_alert = st.checkbox("Detect Head Down", value=True)
    sound_option = st.radio("Select Alert Sound", ["beep", "buzzer", "horn"])

# Streamlit Camera Input
camera_input = st.camera_input("Capture a photo")

if camera_input:
    # Convert the captured image to PIL format
    image = Image.open(camera_input)
    image = np.array(image)  # Convert to NumPy array for model processing

    # Pass the image to the Hugging Face model for classification
    results = fatigue_model(image)

    # Process the model's output and trigger alerts
    if "fatigue" in results[0]['label']:  # Assuming the model can classify "fatigue"
        play_sound(f"{sound_option}.wav")  # Play the selected sound if fatigue is detected
        st.write("Fatigue detected! Alert triggered.")

    # Display the image and model results
    st.image(image, caption="Captured Image", use_column_width=True)
    st.write("Model Prediction: ", results)
