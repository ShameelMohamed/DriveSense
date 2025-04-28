import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import folium
from streamlit_folium import st_folium
import requests

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
            if not hasattr(st.secrets, "firebase"):
                st.error("Firebase configuration not found in secrets!")
                return False
            
            # Create credentials dictionary
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
            
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred)
            return True
        except Exception as e:
            st.error(f"Firebase initialization error: {str(e)}")
            return False
    return True

if not initialize_firebase():
    st.stop()

db = firestore.client()

# Initialize session state
if "locations" not in st.session_state:
    st.session_state.locations = []
if "route_coords" not in st.session_state:
    st.session_state.route_coords = None

# Improved reset function
def reset_markers():
    st.session_state.locations = []
    st.session_state.route_coords = None
    # Use success message instead of rerun
    st.success("Markers reset successfully!")

# Reset markers button
if st.button("Reset Markers"):
    reset_markers()

# Initialize map
map_center = [20.5937, 78.9629]  # Default center: India
m = folium.Map(location=map_center, zoom_start=5)

# Add existing markers
for idx, loc in enumerate(st.session_state.locations):
    label = "Start" if idx == 0 else "Destination"
    folium.Marker(location=loc, popup=label, icon=folium.Icon(color="blue")).add_to(m)

# Display the first map
map_data = st_folium(m, height=600, width="100%", key="main_map")

# Capture clicked points
if map_data and map_data.get("last_clicked"):
    lat, lng = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
    if len(st.session_state.locations) < 2:
        st.session_state.locations.append((lat, lng))
        # Use success message instead of rerun
        st.success(f"Location {len(st.session_state.locations)} set!")

# Display selected locations
if len(st.session_state.locations) == 2:
    st.write(f"🔹 Start: {st.session_state.locations[0]}")
    st.write(f"🔹 Destination: {st.session_state.locations[1]}")
else:
    st.write("Click two points on the map to set the Start and Destination.")

# Route type selection
route_type = st.radio("Select Route Type", ["Shortest Route", "Safest Route"])

# Function to fetch hazard locations
def fetch_hazard_locations():
    try:
        hazards = []
        docs = db.collection("uploads").stream()
        for doc in docs:
            data = doc.to_dict()
            if "gps_location" in data:
                try:
                    lat, lon = map(float, data["gps_location"].split(","))
                    img_url = data.get("image_url", "")
                    hazards.append((lat, lon, img_url))
                except ValueError:
                    continue
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
                buffer_size = 0.001
                polygon = [[
                    [lon - buffer_size, lat - buffer_size],
                    [lon + buffer_size, lat - buffer_size],
                    [lon + buffer_size, lat + buffer_size],
                    [lon - buffer_size, lat + buffer_size],
                    [lon - buffer_size, lat - buffer_size]
                ]]
                avoid_polygons["coordinates"].append(polygon)
            payload["options"] = {"avoid_polygons": avoid_polygons}

    try:
        response = requests.post(ors_url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if data.get("features"):
            route_coords = [(lat, lng) for lng, lat in data["features"][0]["geometry"]["coordinates"]]
            return route_coords, None
        return None, "No route found"
    except Exception as e:
        return None, f"Route error: {str(e)}"

# Button to calculate and show route
if st.button("Get Route"):
    if len(st.session_state.locations) == 2:
        with st.spinner("Calculating route..."):
            route_coords, error_msg = get_route(
                st.session_state.locations[0],
                st.session_state.locations[1],
                route_type == "Safest Route"
            )
        if route_coords:
            st.session_state.route_coords = route_coords
            st.success("Route calculated!")
        else:
            st.error(error_msg)

# Render final map
if st.session_state.locations:
    route_map = folium.Map(
        location=st.session_state.locations[0],
        zoom_start=12,
        key="route_map"
    )
else:
    route_map = folium.Map(location=map_center, zoom_start=5, key="route_map")

# Add markers
for idx, loc in enumerate(st.session_state.locations):
    label = "Start" if idx == 0 else "Destination"
    folium.Marker(location=loc, popup=label, icon=folium.Icon(color="blue")).add_to(route_map)

# Add hazard markers
for hazard in fetch_hazard_locations():
    lat, lon, img_url = hazard
    popup_html = f'<div style="width:200px"><img src="{img_url}" style="width:100%"><br>Hazard: {lat:.4f}, {lon:.4f}</div>'
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa")
    ).add_to(route_map)

# Add route if available
if st.session_state.route_coords:
    folium.PolyLine(
        st.session_state.route_coords,
        color="blue",
        weight=5,
        opacity=0.7
    ).add_to(route_map)

# Display the final map
st_folium(route_map, height=600, width="100%")
