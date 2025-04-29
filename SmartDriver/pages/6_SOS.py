import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import pandas as pd
import requests

# Set page configuration
st.set_page_config(page_title="SOS", page_icon="🚨", layout="wide")

# Background CSS
background_css = """
<style>
    .stApp {
        background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    header {
        visibility: hidden;
    }
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize session state
if "user_location" not in st.session_state:
    st.session_state.user_location = None
if "map" not in st.session_state:
    st.session_state.map = None

# Function to get current location
def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            loc = data.get("loc", "").split(",")
            return [float(loc[0]), float(loc[1])]
    except:
        pass
    return None

# Sidebar
with st.sidebar:
    st.header("SOS")
    show_hospitals = st.checkbox("Show Hospitals", value=True)
    show_police = st.checkbox("Show Police Stations", value=True)
    
    # Add button to get current location
    if st.button("📍 Get My Current Location"):
        current_location = get_current_location()
        if current_location:
            st.session_state.user_location = current_location
            st.success("Location obtained!")
        else:
            st.error("Could not get your location. Please try again or select location on map.")

# Function to calculate distance
def calculate_distance(point1, point2):
    return geodesic(point1, point2).kilometers

# Function to find nearest location
def find_nearest_location(user_location, locations):
    if not user_location or not locations:
        return None
    
    min_distance = float('inf')
    nearest_location = None
    
    for loc in locations:
        # Handle location data based on its format
        if isinstance(loc.get('location'), dict):
            lat = loc['location'].get('lat')
            lon = loc['location'].get('lon')
        else:
            # If location is stored as a string or list
            try:
                lat, lon = map(float, loc.get('location', '').split(','))
            except:
                continue
        
        if lat and lon:
            distance = calculate_distance(user_location, [lat, lon])
            if distance < min_distance:
                min_distance = distance
                nearest_location = loc
    
    return nearest_location, min_distance

# Create or get map from session state
if st.session_state.map is None:
    trichy_location = [10.7905, 78.7047]  # Trichy coordinates
    st.session_state.map = folium.Map(location=trichy_location, zoom_start=12)

# Fetch data from Firestore
sos_data = db.collection("sos").stream()
locations = []
for doc in sos_data:
    data = doc.to_dict()
    locations.append(data)

# Filter locations based on checkboxes
hospitals = [loc for loc in locations if loc.get('type') == 'hospital']
police_stations = [loc for loc in locations if loc.get('type') == 'police']

# Clear existing markers
keys_to_remove = []
for key in st.session_state.map._children:
    if isinstance(st.session_state.map._children[key], (folium.Marker, folium.PolyLine)):
        keys_to_remove.append(key)

# Remove markers after iteration
for key in keys_to_remove:
    del st.session_state.map._children[key]

# Add markers for hospitals
if show_hospitals:
    for hospital in hospitals:
        # Handle location data based on its format
        if isinstance(hospital.get('location'), dict):
            lat = hospital['location'].get('lat')
            lon = hospital['location'].get('lon')
        else:
            try:
                lat, lon = map(float, hospital.get('location', '').split(','))
            except:
                continue
        
        if lat and lon:
            # Get image URL
            image_url = hospital.get('image', '')
            
            popup_html = f"""
            <div style="text-align: center;">
                <img src="{image_url}" width="200px"><br>
                <b>🏥 {hospital.get('name', '')}</b><br>
                Hospital
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='red', icon='hospital', prefix='fa')
            ).add_to(st.session_state.map)

# Add markers for police stations
if show_police:
    for police in police_stations:
        # Handle location data based on its format
        if isinstance(police.get('location'), dict):
            lat = police['location'].get('lat')
            lon = police['location'].get('lon')
        else:
            try:
                lat, lon = map(float, police.get('location', '').split(','))
            except:
                continue
        
        if lat and lon:
            # Get image URL
            image_url = police.get('image', '')
            
            popup_html = f"""
            <div style="text-align: center;">
                <img src="{image_url}" width="200px"><br>
                <b>👮 {police.get('name', '')}</b><br>
                Police Station
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='building', prefix='fa')
            ).add_to(st.session_state.map)

# Display map
map_data = st_folium(st.session_state.map, height=600, width="100%")

# Handle map clicks
if map_data and map_data["last_clicked"]:
    st.session_state.user_location = [map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]]

# If user location is set (either by clicking or current location)
if st.session_state.user_location:
    # Add marker for user location
    folium.Marker(
        location=st.session_state.user_location,
        popup="Your Location",
        icon=folium.Icon(color='green', icon='user', prefix='fa')
    ).add_to(st.session_state.map)
    
    # Find nearest hospital if selected
    if show_hospitals:
        nearest_hospital, hospital_distance = find_nearest_location(st.session_state.user_location, hospitals)
        if nearest_hospital:
            st.success(f"Nearest Hospital: {nearest_hospital['name']} ({hospital_distance:.2f} km away)")
            
            # Get hospital coordinates
            if isinstance(nearest_hospital.get('location'), dict):
                hospital_lat = nearest_hospital['location'].get('lat')
                hospital_lon = nearest_hospital['location'].get('lon')
            else:
                try:
                    hospital_lat, hospital_lon = map(float, nearest_hospital.get('location', '').split(','))
                except:
                    hospital_lat, hospital_lon = None, None
            
            if hospital_lat and hospital_lon:
                # Add line to nearest hospital
                folium.PolyLine(
                    locations=[st.session_state.user_location, [hospital_lat, hospital_lon]],
                    color='red',
                    weight=2,
                    opacity=0.8
                ).add_to(st.session_state.map)
    
    # Find nearest police station if selected
    if show_police:
        nearest_police, police_distance = find_nearest_location(st.session_state.user_location, police_stations)
        if nearest_police:
            st.success(f"Nearest Police Station: {nearest_police['name']} ({police_distance:.2f} km away)")
            
            # Get police station coordinates
            if isinstance(nearest_police.get('location'), dict):
                police_lat = nearest_police['location'].get('lat')
                police_lon = nearest_police['location'].get('lon')
            else:
                try:
                    police_lat, police_lon = map(float, nearest_police.get('location', '').split(','))
                except:
                    police_lat, police_lon = None, None
            
            if police_lat and police_lon:
                # Add line to nearest police station
                folium.PolyLine(
                    locations=[st.session_state.user_location, [police_lat, police_lon]],
                    color='blue',
                    weight=2,
                    opacity=0.8
                ).add_to(st.session_state.map) 