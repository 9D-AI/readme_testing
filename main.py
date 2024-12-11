from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

app = FastAPI()

class RecommendationInput(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    menstrual_cycle_length: int
    average_period_duration: int
    flow_intensity: str
    pre_existing_conditions: list
    dietary_preferences: list
    fitness_goals: str
    location: str

@app.post("/recommendations")
async def generate_recommendation(data: RecommendationInput):

    api_key = os.getenv("GOOGLE_API_KEY")
    # Example LLM prompt construction
    prompt = f"""
    Generate a personalized fitness and diet recommendation for a {data.age}-year-old {data.gender}, height {data.height}, 
    weight {data.weight}, based in {data.location}. Their fitness goal is {data.fitness_goals}.
    Menstrual cycle details: {data.menstrual_cycle_length}-day cycle, {data.average_period_duration}-day duration, {data.flow_intensity} flow.
    Conditions: {', '.join(data.pre_existing_conditions)}. Diet: {', '.join(data.dietary_preferences)}.
    """
    # Call to LLM
    llm = ChatGoogleGenerativeAI(api_key=api_key,model="gemini-1.5-flash-8b",temperature=0.7, top_p=0.85)
    response = llm.invoke(prompt)
    return {"recommendation": response.content}

if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
