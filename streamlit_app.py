import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Set Google API Key


if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
def initialize_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API Key is not set.")
        return None
    return ChatGoogleGenerativeAI(
        api_key=api_key,
        model="gemini-1.5-flash-8b",
        temperature=0.7,
        top_p=0.85
    )

# Generate Recommendation
def generate_recommendation(llm, payload):
    prompt = f"""
    Generate a personalized fitness and diet recommendation for a {payload['age']}-year-old {payload['gender']}, 
    height {payload['height']} ft, weight {payload['weight']} lbs, based in {payload['location']}. 
    Their fitness goal is {payload['fitness_goals']}.
    Menstrual cycle details: {payload['menstrual_cycle_length']}-day cycle, 
    {payload['average_period_duration']}-day duration, {payload['flow_intensity']} flow.
    Conditions: {', '.join(payload['pre_existing_conditions'])}. 
    Diet: {', '.join(payload['dietary_preferences'])}.
    """
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        st.error(f"Error generating recommendation: {e}")
        return None

# Streamlit App
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
    llm = initialize_llm()
    if llm:
        # Prepare Payload
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
        recommendation = generate_recommendation(llm, payload)
        if recommendation:
            st.success("Your Personalized Recommendation:")
            st.write(recommendation)