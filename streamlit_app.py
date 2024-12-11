import streamlit as st
import requests

# Streamlit App Title
st.title("Women's Fitness Recommendation Demo")

# Input Form
with st.form("fitness_form"):
    st.header("Enter Your Details")
    
    # User Demographics
    age = st.number_input("Age", min_value=18, max_value=45, value=25, step=1)
    gender = st.selectbox("Gender", options=["female"], disabled=True)
    height = st.number_input("Height (in feet)", min_value=4.0, max_value=7.0, value=5.4, step=0.1)
    weight = st.number_input("Weight (in lbs)", min_value=80.0, max_value=300.0, value=160.0, step=1.0)
    location = st.text_input("Location", value="New York")
    
    # Health Profile
    menstrual_cycle_length = st.number_input("Menstrual Cycle Length (in days)", min_value=21, max_value=35, value=28)
    average_period_duration = st.number_input("Average Period Duration (in days)", min_value=2, max_value=10, value=5)
    flow_intensity = st.selectbox("Flow Intensity", options=["light", "medium", "heavy"])
    pre_existing_conditions = st.multiselect(
        "Pre-existing Conditions", 
        options=["PCOS", "endometriosis", "diabetes", "hypertension", "none"]
    )
    dietary_preferences = st.multiselect(
        "Dietary Preferences", 
        options=["vegetarian", "vegan", "keto", "gluten-free", "none"]
    )
    
    # Fitness Goals
    fitness_goals = st.selectbox("Fitness Goals", options=["weight loss", "endurance", "flexibility", "muscle gain"])

    # Submit Button
    submit_button = st.form_submit_button("Get Recommendation")

# Handle Form Submission
if submit_button:
    # API Payload
    payload = {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "menstrual_cycle_length": menstrual_cycle_length,
        "average_period_duration": average_period_duration,
        "flow_intensity": flow_intensity,
        "pre_existing_conditions": pre_existing_conditions if pre_existing_conditions else ["none"],
        "dietary_preferences": dietary_preferences if dietary_preferences else ["none"],
        "fitness_goals": fitness_goals,
        "location": location
    }

    # API Call
    try:
        api_url = "http://localhost:8000/recommendations"  # Replace with your API URL
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            recommendation = response.json().get("recommendation", "No recommendation available.")
            st.success("Your Personalized Recommendation:")
            st.write(recommendation)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
