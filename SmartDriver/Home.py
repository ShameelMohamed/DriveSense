import streamlit as st

# Set page configuration
st.set_page_config(page_title="Drive Sense", page_icon="🚗", layout="wide", initial_sidebar_state="collapsed")

# Add logo to sidebar using the provided URL
st.sidebar.image("logo.jpg", use_column_width=True)


# Enhanced and Responsive CSS
background_css = """
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* Apply font globally */
html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
}

/* Background Image */
.stApp {
    background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    padding: 0 16px;
}

/* Hide Streamlit header */
header {
    visibility: hidden;
}

/* --- CARD STYLING --- */
.card { 
  position: relative;
  width: 260px;
  height: 280px;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  margin: 10px;
  display: inline-block;
  background-color: #000;
  box-shadow: 0 4px 24px rgba(80, 0, 128, 0.18);
  animation: fadeInUp 0.8s ease forwards;
  opacity: 0;
  transition: box-shadow 0.3s, transform 0.3s;
}
.card:hover, .card:focus {
  box-shadow: 0 8px 32px rgba(80, 0, 128, 0.28);
  transform: translateY(-4px) scale(1.03);
}
.card img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(75%);
  z-index: 0;
  transition: transform 0.5s ease;
}
.card:hover img, .card:focus img {
  transform: scale(1.1);
  filter: brightness(50%);
}
.card-title {
  position: absolute;
  bottom: 70px;
  left: 0;
  right: 0;
  text-align: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  z-index: 2;
}
.card-text {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  color: white;
  font-size: 14px;
  padding: 0 10px;
  z-index: 2;
}
.card-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #8000ff;
  color: white;
  padding: 10px 20px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: bold;
  font-size: 16px;
  opacity: 0;
  z-index: 3;
}
.card:hover .card-button {
  opacity: 1;
}

/* Entrance Animation */
@keyframes fadeInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive Layout */
@media (max-width: 1024px) {
  .card { width: 240px; height: 260px; }
}
@media (max-width: 600px) {
  .card { width: 220px; height: 240px; }
}

/* Cards row */
.cards-row {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 16px 0;
}
.cards-row::-webkit-scrollbar {
  height: 8px;
}
.cards-row::-webkit-scrollbar-thumb {
  background: #8000ff33;
  border-radius: 4px;
}

/* --- WELCOME TEXT ANIMATION --- */
.welcome-container {
    text-align: center;
    margin: 30px 0;
    overflow: hidden;
}
.welcome-title {
  font-size: 3.5rem;
  color: white;
  font-weight: 800;
  animation: vehicleMove 5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
  white-space: nowrap;
}
.drive-sense {
  margin-left: 5rem;
}
.welcome-subtitle {
  color: #f0f0f0;
  font-size: 1.8rem;
  font-weight: 600;
}
.welcome-text {
  color: #e0e0e0;
  font-size: 1.3rem;
  font-weight: 500;
}

/* Welcome animation */
@keyframes vehicleMove {
  0% { transform: translateX(-100%); }
  40% { transform: translateX(-10%); }
  50% { transform: translateX(0%); }
  60% { transform: translateX(10%); }
  100% { transform: translateX(200%); }
}
</style>
"""

# Inject the CSS into the page
st.markdown(background_css, unsafe_allow_html=True)

# Centered Welcome Section
st.markdown("""
<div class="welcome-container">
    <div class="welcome-title-container">
        <h1 class="welcome-title">Welcome To</h1>
        <h1 class="welcome-title drive-sense">DriveSense!</h1>
    </div>
    <h3 class="welcome-subtitle">Your All-in-One Road Safety App</h3>
    <p class="welcome-text">Swipe & Choose a Feature Below to Get Started.</p>
</div>
""", unsafe_allow_html=True)

# Cards Section
st.markdown("""
<div class="cards-row">
  <a href="RoadHazards" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://img.freepik.com/free-photo/road-warning-signs-set_23-2147627612.jpg" alt="Road Hazards">
      <div class="card-title">Road Hazards</div>
      <div class="card-text">Report or View Live Hazards</div>
    </div>
  </a>

  <a href="FatigueDetection" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://img.freepik.com/free-photo/fatigue-driver_23-2147627611.jpg" alt="Fatigue Detection">
      <div class="card-title">Fatigue Detection</div>
      <div class="card-text">Check Driver Alertness</div>
    </div>
  </a>

  <a href="AccidentPrevention" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://img.freepik.com/free-photo/accident-prevention_23-2147627610.jpg" alt="Accident Prevention">
      <div class="card-title">Accident Prevention</div>
      <div class="card-text">AI Insights for Safer Driving</div>
    </div>
  </a>
</div>
""", unsafe_allow_html=True)
