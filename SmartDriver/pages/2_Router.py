import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import folium
from streamlit_folium import st_folium
import requests
import json

st.set_page_config(page_title="Route Planner", page_icon="🗺️", layout="wide", initial_sidebar_state="collapsed")

# Background styling
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

# OpenRouteService API Key
ORS_API_KEY = "5b3ce3597851110001cf6248e6cfd54b45cc4191bcde2aa3dc9e4a67"

# Initialize Firebase with enhanced error handling
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Debug: Show which secrets are available
            if 'firebase' not in st.secrets:
                st.error("Firebase secrets not found in Streamlit secrets!")
                return False
            
            # Create credentials dictionary directly from secrets
            firebase_config = {
                "type": st.secrets.firebase.type,
                "project_id": st.secrets.firebase.project_id,
                "private_key_id": st.secrets.firebase.private_key_id,
                "private_key": st.secrets.firebase.private_key.replace("\\n", "\n"),
                "client_email": st.secrets.firebase.client_email,
                "client_id": st.secrets.firebase.client_id,
                "auth_uri": st.secrets.firebase.auth_uri,
                "token_uri": st.secrets.firebase.token_uri,
                "auth_provider_x509_cert_url": st.secrets.firebase.auth_provider_x509_cert_url,
                "client_x509_cert_url": st.secrets.firebase.client_x509_cert_url,
                "universe_domain": st.secrets.firebase.universe_domain
            }
            
            # Initialize Firebase
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
            return True
        except Exception as e:
            st.error(f"Firebase initialization failed: {str(e)}")
            st.error("Please check your Firebase credentials in Streamlit Secrets")
            return False
    return True

if not initialize_firebase():
    st.stop()  # Stop the app if Firebase fails to initialize

db = firestore.client()

# App title
st.title("🚗 SmartDriver - Route Planner with Hazard Warnings")

# Initialize session state
if "locations" not in st.session_state:
    st.session_state.locations = []
if "route_coords" not in st.session_state:
    st.session_state.route_coords = None

# Reset markers button
if st.button("Reset Markers"):
    st.session_state.locations = []
    st.session_state.route_coords = None
    st.experimental_rerun()

# Initialize map (Consistent Zoom)
map_center = [20.5937, 78.9629]  # Default center: India
m = folium.Map(location=map_center, zoom_start=5)

# Add existing markers
for idx, loc in enumerate(st.session_state.locations):
    label = "Start" if idx == 0 else "Destination"
    folium.Marker(location=loc, popup=label, icon=folium.Icon(color="blue")).add_to(m)

# Display the first map (Fixed height)
map_data = st_folium(m, height=600, width="100%", key="main_map")

# Capture clicked points
if map_data and map_data.get("last_clicked"):
    lat, lng = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
    if len(st.session_state.locations) < 2:
        st.session_state.locations.append((lat, lng))
        st.experimental_rerun()

# Display selected locations
if len(st.session_state.locations) == 2:
    st.write(f"🔹 *Start:* {st.session_state.locations[0]}")
    st.write(f"🔹 *Destination:* {st.session_state.locations[1]}")
else:
    st.write("Click two points on the map to set the Start and Destination.")

# Route type selection
route_type = st.radio("Select Route Type", ["Shortest Route", "Safest Route"])

# Function to fetch hazard locations from Firebase
def fetch_hazard_locations():
    try:
        hazard_docs = db.collection("uploads").stream()
        hazards = []
        for doc in hazard_docs:
            data = doc.to_dict()
            if "gps_location" in data:
                try:
                    lat, lon = map(float, data["gps_location"].split(","))
                    img_url = data.get("image_url", "")
                    hazards.append((lat, lon, img_url))
                except Exception as e:
                    st.warning(f"Couldn't parse location for hazard: {str(e)}")
        return hazards
    except Exception as e:
        st.error(f"Error fetching hazards: {str(e)}")
        return []

# Function to fetch the route
def get_route(start, end, avoid_hazards=False):
    if not start or not end:
        return None, "Select both start and destination points."

    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {"Authorization": ORS_API_KEY, "Content-Type": "application/json"}

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

            for hazard in hazards:
                lat, lon = hazard[0], hazard[1]
                # Small square buffer around each hazard
                buffer_size = 0.001  # ~500m
                polygon = [[
                    [lon - buffer_size, lat - buffer_size],
                    [lon + buffer_size, lat - buffer_size],
                    [lon + buffer_size, lat + buffer_size],
                    [lon - buffer_size, lat + buffer_size],
                    [lon - buffer_size, lat - buffer_size]  # Close the polygon
                ]]
                avoid_polygons["coordinates"].append(polygon)
            
            payload["options"] = {"avoid_polygons": avoid_polygons}

    try:
        response = requests.post(ors_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        if "features" in response_json and response_json["features"]:
            route_data = response_json["features"][0]["geometry"]["coordinates"]
            route_coords = [(lat, lng) for lng, lat in route_data]
            return route_coords, None
        else:
            return None, "No route features found in response"
            
    except Exception as e:
        return None, f"Route API error: {str(e)}"

# Button to calculate and show route
if st.button("Get Route"):
    if len(st.session_state.locations) == 2:
        start, end = st.session_state.locations
        avoid_hazards = route_type == "Safest Route"
        
        with st.spinner("Calculating route..."):
            route_coords, error_msg = get_route(start, end, avoid_hazards)

        if route_coords:
            st.session_state.route_coords = route_coords
            st.success("Route calculated successfully!")
        else:
            st.error(error_msg)

# Render updated map with route
route_map = folium.Map(
    location=st.session_state.locations[0] if st.session_state.locations else map_center,
    zoom_start=5,
    key="route_map"
)

# Add markers
for idx, loc in enumerate(st.session_state.locations):
    label = "Start" if idx == 0 else "Destination"
    folium.Marker(location=loc, popup=label, icon=folium.Icon(color="blue")).add_to(route_map)

# Add hazard markers
hazard_locations = fetch_hazard_locations()
for hazard in hazard_locations:
    lat, lon, img_url = hazard
    popup_html = f"""
    <div style="text-align: center;">
        <img src="{img_url}" width="200px"><br>
        <b>🚧 Hazard Location</b><br>
        {lat}, {lon}
    </div>
    """
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
    ).add_to(route_map)

# Add route if available
if st.session_state.route_coords:
    folium.PolyLine(
        st.session_state.route_coords, 
        color="blue", 
        weight=5, 
        opacity=0.7,
        tooltip="Calculated Route"
    ).add_to(route_map)

# Display the final map
st_folium(route_map, height=600, width="100%", key="final_map")
