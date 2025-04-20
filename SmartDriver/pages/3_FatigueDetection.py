import streamlit as st
#import cv2

st.title("Camera Test with OpenCV")

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    st.image(frame, channels="BGR")
else:
    st.error("Camera not accessible.")
cap.release()
