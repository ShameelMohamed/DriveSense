# app.py

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import folium
from streamlit_folium import st_folium
import requests
import json
import os

# --- Streamlit Config ---
st.set_page_config(
    page_title="Route Planner",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Background Styling ---
st.markdown("""
<style>
    .stApp {
        background-image: url('https://i.pinimg.com/originals/6d/46/f9/6d46f977733e6f9a9fa8f356e2b3e0fa.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- Constants ---
ORS_API_KEY = st.secrets["ORS_API_KEY"]  # API Key stored safely in Streamlit Secrets
FIREBASE_CREDENTIALS = st.secrets["firebase_credentials"]  # Loaded from Streamlit Secrets

# --- Initialize Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(FIREBASE_CREDENTIALS))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Session State ---
if "locations" not in st.session_state:
    st.session_state.locations = []
if "route_coords" not in st.session_state:
    st.session_state.route_coords = None

# --- Page Title ---
st.title("🚗 SmartDriver - Route Planner with Hazard Warnings")

# --- Reset Button ---
if st.button("Reset Markers"):
    st.session_state.locations = []
    st.session_state.route_coords = None

# --- Initialize Base Map ---
map_center = [20.5937, 78.9629]  # Centered on India
m = folium.Map(location=map_center, zoom_start=5)

# --- Add Existing Markers ---
for idx, loc in enumerate(st.session_state.locations):
    label = "Start" if idx == 0 else "Destination"
    folium.Marker(location=loc, popup=label, icon=folium.Icon(color="blue")).add_to(m)

# --- Display Map (First Time) ---
map_data = st_folium(m, height=600, width="100%")

# --- Capture User Clicks ---
if map_data and map_data.get("last_clicked"):
    lat, lng = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
    if len(st.session_state.locations) < 2:
        st.session_state.locations.append((lat, lng))

# --- Show Selected Points ---
if len(st.session_state.locations) == 2:
    st.write(f"🔹 **Start:** {st.session_state.locations[0]}")
    st.write(f"🔹 **Destination:** {st.session_state.locations[1]}")
else:
    st.info("Click two points on the map to set the Start and Destination.")

# --- Route Type ---
route_type = st.radio("Select Route Type", ["Shortest Route", "Safest Route"])

# --- Fetch Hazards ---
@st.cache_data
def fetch_hazard_locations():
    hazards = []
    for doc in db.collection("uploads").stream():
        data = doc.to_dict()
        if "gps_location" in data:
            lat, lon = map(float, data["gps_location"].split(","))
            img_url = data.get("image_url", "")
            hazards.append((lat, lon, img_url))
    return hazards

# --- Get Route ---
def get_route(start, end, avoid_hazards=False):
    if not start or not end:
        return None, "Select both start and destination points."

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "coordinates": [[start[1], start[0]], [end[1], end[0]]],
        "radiuses": [500, 500],
    }

    if avoid_hazards:
        hazards = fetch_hazard_locations()
        if hazards:
            avoid_polygons = {
                "type": "MultiPolygon",
                "coordinates": []
            }
            buffer_size = 0.001  # ~500m radius
            for lat, lon, _ in hazards:
                polygon = [[
                    [lon - buffer_size, lat - buffer_size],
                    [lon + buffer_size, lat - buffer_size],
                    [lon + buffer_size, lat + buffer_size],
                    [lon - buffer_size, lat + buffer_size],
                    [lon - buffer_size, lat - buffer_size]
                ]]
                avoid_polygons["coordinates"].append(polygon)
            payload["options"] = {"avoid_polygons": avoid_polygons}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        geojson = response.json()
        if "features" in geojson and geojson["features"]:
            coords = geojson["features"][0]["geometry"]["coordinates"]
            route = [(lat, lon) for lon, lat in coords]
            return route, None

    return None, f"Route not found. Error: {response.text}"

# --- Route Button ---
if st.button("Get Route"):
    if len(st.session_state.locations) == 2:
        start, end = st.session_state.locations
        avoid_hazards = route_type == "Safest Route"
        route_coords, error = get_route(start, end, avoid_hazards)
        if route_coords:
            st.session_state.route_coords = route_coords
        else:
            st.error(error)

# --- Render Final Map ---
final_map = folium.Map(
    location=st.session_state.locations[0] if st.session_state.locations else map_center,
    zoom_start=5
)

# Add Markers
for idx, loc in enumerate(st.session_state.locations):
    label = "Start" if idx == 0 else "Destination"
    folium.Marker(location=loc, popup=label, icon=folium.Icon(color="blue")).add_to(final_map)

# Add Hazards
for lat, lon, img_url in fetch_hazard_locations():
    popup_html = f"""
    <div style="text-align: center;">
        <img src="{img_url}" width="200px"><br>
        <b>🚧 Hazard Location</b><br>{lat}, {lon}
    </div>
    """
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
    ).add_to(final_map)

# Add Route
if st.session_state.route_coords:
    folium.PolyLine(
        st.session_state.route_coords,
        color="blue",
        weight=5,
        opacity=0.7
    ).add_to(final_map)

# Display Final Map
st_folium(final_map, height=600, width="100%")
