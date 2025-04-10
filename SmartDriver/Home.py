import streamlit as st
from PIL import Image  # Import for logo

# Set page configuration
st.set_page_config(page_title="Drive Sense", page_icon="🚗", layout="wide", initial_sidebar_state="collapsed")

# Add logo to sidebar
logo = Image.open("https://media-hosting.imagekit.io/963a894003644c1d/logo.jpg?Expires=1838884565&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=aOoYDdWn~y2eLbJwkEovyF6eTOlu8S-0t7H2txxkgtubV7c7BoI8rGkDB5Rl6KzDlenUrr898m0xNdnvfOGj4c8bgRCMZKHSkDv49zR9vJKKo0r9aPbKuIQqSXGoHfqSf89ghydzZgUJ~HvdJRpY61kgMgbvZZ7cwj2hE5RqHpmtHSvZyWxNHrvNlnQ3a5GLxmSFWW9LexOkTxlZQqoK41Wjnb4NZPksVBT4QerXCDOnDjZgWfESvhpIK6szK630QTruB5uJXTFPMnmxnUDxXGdvLuNL9BNn9xbAYbB-QpJ5DLE4vvaaJlWbj~An8kENrqV2tyXm4OUO6nn9M198qg__")
st.sidebar.image(logo)

# Define custom CSS for card styling and background image
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
}

/* Hide Streamlit header */
header {
    visibility: hidden;
}

/* Card Styles */
.card {
  position: relative;
  width: 260px;
  height: 260px;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  margin: 20px;
  display: inline-block;
  background-color: #000;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  animation: fadeInUp 0.8s ease forwards;
  opacity: 0;
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

.card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  transition: background 0.3s ease;
}

.card:hover::before {
  background: rgba(0, 0, 0, 0.5);
}

.card img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
  filter: brightness(75%);
  z-index: 0;
}

.card:hover img {
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
  transition: opacity 0.3s ease;
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
  transition: opacity 0.3s ease;
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
  z-index: 3;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card-button:hover {
  background: white;
  color: #8000ff;
  transition: all 0.25s ease;
}

.card:hover .card-button {
  opacity: 1;
}

/* Responsive Layout */
@media (max-width: 768px) {
  .card {
    width: 100% !important;
    height: auto;
    margin: 10px 0;
  }
}

.st-emotion-cache-seewz2 a {
  text-decoration: none;
  color: white;
}
</style>
"""

# Inject the CSS into the page
st.markdown(background_css, unsafe_allow_html=True)

# Page title
st.subheader("")
st.title("Welcome to DriveSense !")
st.subheader("Your All-in-One Road Safety App")
st.subheader("")

# Create columns for horizontal layout
col1, col2, col3, col4 = st.columns(4)

# Card 1: Road Hazards
with col1:
    st.markdown(
        """
        <div class="card" onclick="window.location.href='RoadHazards'">
            <img src="https://media.istockphoto.com/id/538686713/photo/cracked-asphalt-after-earthquake.jpg?s=612x612&w=0&k=20&c=SbzwfmL_xf0rgZ4spkJPZ6wD6tR4AzkYEeA5iyg-_u4=" alt="Road Hazards">
            <div class="card-title">Road Hazards</div>
            <div class="card-text">Identify potential risks on your route and drive safer.</div>
            <a class="card-button" href="RoadHazards" onclick="window.location.href='RoadHazards'; return false;">Explore</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 2: Route Planner
with col2:
    st.markdown(
        """
        <div class="card" onclick="window.location.href='Router'">
            <img src="https://media.istockphoto.com/id/182150881/photo/mountain-highway-towards-the-clouds-haleakala-maui-hawaii.jpg?s=612x612&w=0&k=20&c=ZNAD3N_dqjPHO34ziErnMkqYfiebHDUyaP8226knUtg=" alt="Route Planner">
            <div class="card-title">Route Planner</div>
            <div class="card-text">Plan short and safe routes with advanced route planner.</div>
            <div class="card-button" onclick="window.location.href='RoadHazards'">Explore</div>

        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 3: Fatigue Detection
with col3:
    st.markdown(
        """
        <div class="card" onclick="window.location.href='FatigueDetection'">
            <img src="https://img.freepik.com/premium-photo/dashboard-car-shows-dashboard-with-controls-dashboard_916191-384838.jpg" alt="Fatigue Detection">
            <div class="card-title">Fatigue Detection</div>
            <div class="card-text">Stay alert while driving with fatigue monitoring.</div>
            <a class="card-button" href="FatigueDetection" onclick="window.location.href='FatigueDetection'; return false;">Explore</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Card 4: AI Speech Bot
with col4:
    st.markdown(
        """
        <div class="card" onclick="window.location.href='Speech'">
            <img src="https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/14202/production/_108243428_gettyimages-871148930.jpg" alt="AI Speech Bot">
            <div class="card-title">AI Speech Bot</div>
            <div class="card-text">Get real-time road safety advice from our speech bot.</div>
            <a class="card-button" href="Speech" onclick="window.location.href='Speech'; return false;">Explore</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
