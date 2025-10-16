from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from services.llm_client import GeminiLLM

app = FastAPI(
    title="SkillPath AI Backend",
    description="Generates personalized 7-day learning plans",
    version="0.1"
)

class PlanRequest(BaseModel):
    topic: str

class Resource(BaseModel):
    type: str
    title: str
    url: str

class DayPlan(BaseModel):
    day: str
    topic: str
    mini_challenge: str
    reasoning: str
    resources: List[Resource]

@app.post("/generate_plan", response_model=List[DayPlan])
def generate_plan(request: PlanRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    try:
        llm = GeminiLLM()
        plan = llm.generate_learning_plan(request.topic)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
