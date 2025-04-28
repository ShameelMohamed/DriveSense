import streamlit as st

# Set page configuration
st.set_page_config(page_title="Drive Sense", page_icon="🚗", layout="wide", initial_sidebar_state="collapsed")

# Add logo to sidebar using the provided URL
st.sidebar.image("https://media-hosting.imagekit.io/963a894003644c1d/logo.jpg?Expires=1838884565&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=aOoYDdWn~y2eLbJwkEovyF6eTOlu8S-0t7H2txxkgtubV7c7BoI8rGkDB5Rl6KzDlenUrr898m0xNdnvfOGj4c8bgRCMZKHSkDv49zR9vJKKo0r9aPbKuIQqSXGoHfqSf89ghydzZgUJ~HvdJRpY61kgMgbvZZ7cwj2hE5RqHpmtHSvZyWxNHrvNlnQ3a5GLxmSFWW9LexOkTxlZQqoK41Wjnb4NZPksVBT4QerXCDOnDjZgWfESvhpIK6szK630QTruB5uJXTFPMnmxnUDxXGdvLuNL9BNn9xbAYbB-QpJ5DLE4vvaaJlWbj~An8kENrqV2tyXm4OUO6nn9M198qg__", use_container_width=True)



# Enhanced and Responsive CSS
background_css = """
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

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

/* Card Styles */
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

.card:hover::before, .card:focus::before {
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
  font-size: 16px;
}

.card-button:hover, .card-button:focus {
  background: white;
  color: #8000ff;
  transition: all 0.25s ease;
}

.card:hover .card-button, .card:focus .card-button {
  opacity: 1;
}

/* Enhanced Responsive Layout */
@media (max-width: 1024px) {
  .card {
    width: 240px !important;
    max-width: 240px;
    height: 260px;
    margin: 8px !important;
  }
  .st-emotion-cache-1r6slb0 {
    flex-direction: column !important;
    align-items: center !important;
  }
}
@media (max-width: 600px) {
  .card {
    width: 220px !important;
    max-width: 220px;
    height: 240px;
    margin: 6px !important;
  }
  .card-title { font-size: 16px; }
  .card-text { font-size: 12px; }
  .card-button { padding: 8px 14px; font-size: 14px; }
}

.st-emotion-cache-seewz2 a {
  text-decoration: none;
  color: white;
}

/* Updated cards-row CSS with reduced gap */
.cards-row {
  display: flex;
  flex-direction: row;
  gap: 8px;
  justify-content: flex-start;
  align-items: stretch;
  overflow-x: auto;
  padding: 16px 0;
  margin: -16px -16px 24px -16px;
  scrollbar-width: thin;
  width: calc(100% + 32px);
}
.cards-row::-webkit-scrollbar {
  height: 8px;
}
.cards-row::-webkit-scrollbar-thumb {
  background: #8000ff33;
  border-radius: 4px;
}
.card {
  min-width: 260px;
  max-width: 260px;
  flex: 0 0 auto;
}

/* Optional: Add horizontal scroll to columns on small screens */
.st-emotion-cache-13k62yr {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
}

/* Enhanced Speed Animation */
@keyframes speedIn {
  0% {
    transform: translateX(-100%) scale(0.5);
    opacity: 0;
    filter: blur(10px);
  }
  50% {
    transform: translateX(5%) scale(1.1);
    opacity: 0.8;
    filter: blur(2px);
  }
  75% {
    transform: translateX(-2%) scale(0.95);
    opacity: 0.9;
    filter: blur(0px);
  }
  100% {
    transform: translateX(0) scale(1);
    opacity: 1;
    filter: blur(0px);
  }
}

/* New speed trail animations */
@keyframes leftTrail {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    transform: translateX(100%);
    opacity: 0;
  }
}

@keyframes rightTrail {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    transform: translateX(-100%);
    opacity: 0;
  }
}

/* Update vehicle movement animation for Welcome to */
@keyframes vehicleMove {
  0% {
    transform: translateX(-200%) scale(1);
    opacity: 0;
  }
  5% {
    transform: translateX(-150%) scale(1);
    opacity: 1;
  }
  20% {
    transform: translateX(-100%) scale(1.1);
    opacity: 1;
  }
  40% {
    transform: translateX(-50%) scale(1);
    opacity: 1;
  }
  50% {
    transform: translateX(0%) scale(0.95);
    opacity: 1;
  }
  60% {
    transform: translateX(50%) scale(1);
    opacity: 1;
  }
  80% {
    transform: translateX(100%) scale(1.1);
    opacity: 1;
  }
  95% {
    transform: translateX(300%) scale(1);
    opacity: 0;
  }
  100% {
    transform: translateX(300%) scale(1);
    opacity: 0;
  }
}

/* Enhanced animation for DriveSense */
@keyframes driveSenseMove {
  0% {
    transform: translateX(-250%) scale(1);
    opacity: 0;
  }
  5% {
    transform: translateX(-200%) scale(1);
    opacity: 1;
  }
  15% {
    transform: translateX(-150%) scale(1.2);
    opacity: 1;
  }
  30% {
    transform: translateX(-100%) scale(1);
    opacity: 1;
  }
  40% {
    transform: translateX(-50%) scale(0.95);
    opacity: 1;
  }
  50% {
    transform: translateX(0%) scale(1);
    opacity: 1;
  }
  60% {
    transform: translateX(50%) scale(1.1);
    opacity: 1;
  }
  75% {
    transform: translateX(150%) scale(1.2);
    opacity: 1;
  }
  95% {
    transform: translateX(350%) scale(1);
    opacity: 0;
  }
  100% {
    transform: translateX(350%) scale(1);
    opacity: 0;
  }
}

.welcome-title {
  font-size: 3.5rem;
  color: #ffffff;
  position: relative;
  display: inline-block;
  font-weight: 800;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 
    0 0 5px rgba(255, 255, 255, 0.5),
    0 0 10px rgba(255, 255, 255, 0.3),
    0 0 15px rgba(128, 0, 255, 0.2);
  animation: 
    vehicleMove 10s cubic-bezier(0.4, 0, 0.2, 1) infinite,
    glowPulse 2s ease-in-out infinite;
  white-space: nowrap;
  margin: 0;
  transition: transform 0.3s ease;
}

/* Left side trails - only before text */
.welcome-title::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent,
    rgba(255, 255, 255, 0.8),
    transparent
  );
  transform: translateY(-50%);
  animation: speedTrail 0.5s linear infinite;
  filter: blur(1px);
  box-shadow: none;
}

/* Remove right side trails */
.welcome-title::after {
  display: none;
}

/* Update the road line animation for opposite direction */
@keyframes roadLine {
  0% {
    background-position: 100px 0;
  }
  40% {
    background-position: 40px 0;
  }
  50% {
    background-position: 0 0;  /* Stop point */
  }
  60% {
    background-position: -40px 0;
  }
  100% {
    background-position: -100px 0;
  }
}

/* Update the road line element */
.welcome-container::after {
  content: '';
  position: absolute;
  top: 35%;  /* Moved down from 25% to 35% */
  left: 0;
  right: 0;
  height: 3px;
  background: repeating-linear-gradient(
    90deg,
    #ffffff 0px,
    #ffffff 40px,
    transparent 40px,
    transparent 80px
  );
  transform: translateY(-50%);
  animation: roadLine 0.4s linear infinite;  /* Restored previous speed from 0.2s to 0.4s */
  box-shadow: none;
  z-index: 1;
}

/* Remove the second line */
.welcome-container::before {
  display: none;
}

/* Remove animation from subtitle and text */
.welcome-subtitle {
  color: #f0f0f0;
  font-size: 2.2rem;  /* Increased from 1.8rem to 2.2rem */
  font-weight: 600;
  text-shadow: none;
  margin-top: 1rem;
}

.welcome-text {
  color: #e0e0e0;
  font-size: 1.6rem;  /* Increased from 1.3rem to 1.6rem */
  font-weight: 500;
  text-shadow: none;
  margin-top: 0.5rem;
}

/* Update welcome container to handle the full exit */
.welcome-container {
  position: relative;
  text-align: center;
  margin-bottom: 3rem;
  overflow: hidden;
  padding: 2rem;
  height: auto;
  width: 100%;
  margin-left: 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 15px;
  backdrop-filter: blur(5px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }

}

/* Add a container for the road line */
.road-line-container {
  position: relative;
  width: 100%;
  height: 4px;
  background: rgba(0, 0, 0, 0.3);
  margin: 1rem 0;
  border-radius: 2px;
  overflow: hidden;
}

/* Add styles for the title container and split lines */
.welcome-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  position: relative;
  z-index: 2;
  overflow: hidden;
  perspective: 1000px;
  width: 100vw;  /* Ensure full width for complete exit */
  margin-left: -50vw;  /* Center the container */
  left: 50%;  /* Center the container */
  position: relative;
}

.drive-sense {
  margin-left: 8rem;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 
    0 0 5px rgba(255, 255, 255, 0.5),
    0 0 10px rgba(255, 255, 255, 0.3),
    0 0 15px rgba(128, 0, 255, 0.2);
  margin-top: -0.5rem;
  animation: 
    driveSenseMove 10s cubic-bezier(0.4, 0, 0.2, 1) infinite,
    glowPulse 2s ease-in-out infinite;
  transition: transform 0.3s ease;
}

/* Add a subtle glow animation */
@keyframes glowPulse {
  0% {
    text-shadow: 
      0 0 5px rgba(255, 255, 255, 0.5),
      0 0 10px rgba(255, 255, 255, 0.3),
      0 0 15px rgba(128, 0, 255, 0.2);
  }
  50% {
    text-shadow: 
      0 0 8px rgba(255, 255, 255, 0.6),
      0 0 12px rgba(255, 255, 255, 0.4),
      0 0 18px rgba(128, 0, 255, 0.3);
  }
  100% {
    text-shadow: 
      0 0 5px rgba(255, 255, 255, 0.5),
      0 0 10px rgba(255, 255, 255, 0.3),
      0 0 15px rgba(128, 0, 255, 0.2);
  }
}

/* Update subtitle and text to ensure visibility */
.welcome-subtitle {
  color: #ffffff;
  font-size: 2.2rem;
  font-weight: 600;
  text-shadow: none;
  margin-top: 1rem;
  position: relative;
  z-index: 2;
}

.welcome-text {
  color: #ffffff;
  font-size: 1.6rem;
  font-weight: 500;
  text-shadow: none;
  margin-top: 0.5rem;
  position: relative;
  z-index: 2;
}

/* Add a subtle tilt effect */
.welcome-title:hover, .drive-sense:hover {
  transform: rotateX(5deg) rotateY(5deg);
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

st.markdown("""
<div class="cards-row">
  <a href="RoadHazards" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://media.istockphoto.com/id/538686713/photo/cracked-asphalt-after-earthquake.jpg?s=612x612&w=0&k=20&c=SbzwfmL_xf0rgZ4spkJPZ6wD6tR4AzkYEeA5iyg-_u4=" alt="Road Hazards">
      <div class="card-title">Road Hazards</div>
      <div class="card-text">Identify potential risks on your route and drive safer.</div>
      <div class="card-button">Explore</div>
    </div>
  </a>
  <a href="Router" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://media.istockphoto.com/id/182150881/photo/mountain-highway-towards-the-clouds-haleakala-maui-hawaii.jpg?s=612x612&w=0&k=20&c=ZNAD3N_dqjPHO34ziErnMkqYfiebHDUyaP8226knUtg=" alt="Route Planner">
      <div class="card-title">Route Planner</div>
      <div class="card-text">Plan short and safe routes with advanced route planner.</div>
      <div class="card-button">Explore</div>
    </div>
  </a>
  <a href="FatigueDetection" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://img.freepik.com/premium-photo/dashboard-car-shows-dashboard-with-controls-dashboard_916191-384838.jpg" alt="FatigueDetection">
      <div class="card-title">Fatigue Detection</div>
      <div class="card-text">Stay alert while driving with fatigue monitoring.</div>
      <div class="card-button">Explore</div>
    </div>
  </a>
  <a href="Speech" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/14202/production/_108243428_gettyimages-871148930.jpg" alt="Speech">
      <div class="card-title">Speech</div>
      <div class="card-text">Get real-time road safety advice from our speech bot.</div>
      <div class="card-button">Explore</div>
    </div>
  </a>
  <a href="TODO" style="text-decoration:none;">
    <div class="card" tabindex="0">
      <img src="https://images.squarespace-cdn.com/content/v1/64236014406b577a88f99b3a/2b721232-76f6-42db-b083-a4417e32f70a/microsoft-to-do-feature.jpeg" alt="Speech">
      <div class="card-title">AI To-Do</div>
      <div class="card-text">Let AI plan your trip, so you can focus on what matters!</div>
      <div class="card-button">Explore</div>
    </div>
  </a>
</div>
""", unsafe_allow_html=True)
