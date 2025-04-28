import streamlit as st
import google.generativeai as gen_ai
import re
import time
import random

# --- Setup ---
gen_ai.configure(api_key="AIzaSyByJzlUoKiO1y1xytWczcnQvda9SAwYReo")
model = gen_ai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Tour TODO List Generator", page_icon="🗺", layout="centered")

st.title("🗺 Tour TODO List Generator")
st.caption("Plan your journey smarter with AI-powered TODO lists!")

st.markdown("---")
st.subheader("📝 Enter Your Journey Details")

# Initialize session states
if "todo_lines" not in st.session_state:
    st.session_state.todo_lines = []
if "task_status" not in st.session_state:
    st.session_state.task_status = {}
if "todo_generated" not in st.session_state:
    st.session_state.todo_generated = False
if "current_tip" not in st.session_state:
    st.session_state.current_tip = ""
if "last_updated" not in st.session_state:
    st.session_state.last_updated = time.time()

# Input Form
with st.form(key="journey_form"):
    vehicle = st.text_input("🚗 Vehicle Details", placeholder="e.g., Toyota Camry")
    fuel_consumption = st.text_input("⛽ Fuel Consumption", placeholder="e.g., 7.5 L/100km")
    desired_speed = st.text_input("🏎 Desired Speed (km/h)", placeholder="e.g., 100")
    start_location = st.text_input("📍 Start Location", placeholder="e.g., Hyderabad")
    destination = st.text_input("📍 Destination", placeholder="e.g., Goa")
    
    col1, col2 = st.columns(2)
    with col1:
        generate = st.form_submit_button("✅ Generate TODO List")
    with col2:
        clear = st.form_submit_button("🗑 Clear")

# Generate TODO list
def generate_todo(details):
    prompt = (
        "Generate exactly 10 simple numbered TODO tasks for a journey preparation based on these details:\n"
        f"- Vehicle: {details['vehicle']}\n"
        f"- Fuel consumption: {details['fuel_consumption']}\n"
        f"- Desired speed: {details['desired_speed']} km/h\n"
        f"- Start location: {details['start_location']}\n"
        f"- Destination: {details['destination']}\n"
        "Tasks should be simple, clear, and helpful. No headings, only numbers and tasks."
    )
    try:
        response = model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 300,
                "top_p": 0.8,
                "top_k": 40,
            }
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating TODO: {e}")
        return ""

# Form actions
if generate:
    if not all([vehicle, fuel_consumption, desired_speed, start_location, destination]):
        st.warning("⚠ Please complete all fields.")
    else:
        with st.spinner("Generating TODO list..."):
            todo_text = generate_todo({
                "vehicle": vehicle,
                "fuel_consumption": fuel_consumption,
                "desired_speed": desired_speed,
                "start_location": start_location,
                "destination": destination
            })
            # Store only first 10 lines
            lines = todo_text.splitlines()
            task_lines = [line for line in lines if re.match(r"^\d+[\.\)]", line)]
            st.session_state.todo_lines = task_lines[:10]
            st.session_state.task_status = {task.strip(): False for task in task_lines[:10]}  # Initialize task status
            st.session_state.todo_generated = True  # Mark that todo list is generated

if clear:
    st.session_state.todo_lines = []
    st.session_state.task_status = {}
    st.session_state.todo_generated = False

# Show TODO List
if st.session_state.todo_lines:
    st.markdown("---")
    st.subheader("📋 Your Journey TODO List")

    completed_tasks = 0  # Track completed tasks
    total_tasks = len(st.session_state.todo_lines)

    # Inject CSS to increase checkbox label font size
    st.markdown(
        """
        <style>
        label.css-1q3mhkq.e1cb0a0o2 {  /* This targets the checkbox labels */
            font-size: 20px !important;  /* Increase font size */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for idx, line in enumerate(st.session_state.todo_lines):
        task_text = re.sub(r"^\d+[\.\)]\s*", "", line).strip()

        if task_text not in st.session_state.task_status:
            st.session_state.task_status[task_text] = False

        task_status = st.session_state.task_status[task_text]
        checkbox = st.checkbox(task_text, value=task_status, key=f"task_{idx}")

        if checkbox != task_status:
            st.session_state.task_status[task_text] = checkbox

        if checkbox:
            completed_tasks += 1

    # Calculate and show progress bar
    progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    st.progress(progress / 100)

    st.caption(f"✅ {completed_tasks} of {total_tasks} tasks completed")

# Eco-Friendly Driving Tips (after TODO generated only)
if st.session_state.todo_generated:
    st.markdown("---")
    st.subheader("🌿 Eco-Friendly Driving Tips")

    # Auto refresh every 5 seconds
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=3000, limit=None, key="tip_refresh")

    tips_container = st.empty()

    eco_tips = [
        "Drive smoothly and avoid sudden acceleration and braking.",
        "Keep your tires inflated to the recommended pressure to improve fuel efficiency.",
        "Reduce your speed to save fuel and reduce emissions.",
        "Avoid idling your vehicle for long periods of time.",
        "Carpool or use public transportation when possible to reduce your carbon footprint.",
        "Use cruise control on highways to maintain a steady speed and save gas.",
        "Remove unnecessary weight from your car to improve mileage.",
        "Use the correct engine oil recommended for your car to maximize efficiency."
    ]

    random_tip = random.choice(eco_tips)
    st.session_state.current_tip = random_tip

    tip_html = f"""
    <div style="
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        background-color: #f0fff0;
        color: #2e7d32;
        font-size: 18px;
        margin-top: 10px;
        text-align: center;
    ">
        🌱 <b>Tip:</b> {st.session_state.current_tip}
    </div>
    """

    tips_container.markdown(tip_html, unsafe_allow_html=True)