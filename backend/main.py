from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from services.llm_client import GeminiLLM
from services.serper_client import get_comprehensive_resources, get_limited_resources_for_overview

app = FastAPI(
    title="SkillPath AI Backend",
    description="Generates personalized 7-day learning plans",
    version="0.1"
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "SkillPath AI Backend is running"}

class PlanRequest(BaseModel):
    topic: str

class DetailedDayRequest(BaseModel):
    topic: str
    day_topic: str
    day_number: int

class Resource(BaseModel):
    type: str
    title: str
    url: str
    snippet: Optional[str] = None

class DayPlan(BaseModel):
    day: str
    topic: str
    mini_challenge: str
    reasoning: str
    resources: List[Resource]

class DetailedDayPlan(BaseModel):
    day: str
    topic: str
    detailed_description: str
    learning_objectives: List[str]
    mini_challenge: str
    detailed_challenge: str
    step_by_step_guide: List[str]
    key_concepts: List[str]
    reasoning: str
    estimated_time: str
    difficulty_level: str
    prerequisites: List[str]
    resources: List[Resource]
    next_steps: str

@app.post("/generate_plan", response_model=List[DayPlan])
def generate_plan(request: PlanRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    try:
        llm = GeminiLLM()
        plan = llm.generate_learning_plan(request.topic)
        
        # Enhance resources with Serper API for each day
        for day in plan:
            try:
                # Use limited resources for overview page (1 YouTube, 1 Article, 1 Blog)
                serper_resources = get_limited_resources_for_overview(request.topic, day['topic'])
                # Replace LLM resources with curated Serper resources
                day['resources'] = serper_resources
            except Exception as serper_error:
                print(f"Serper API failed for {day['topic']}: {serper_error}")
                # Continue with LLM-generated resources if Serper fails
                if day.get('resources'):
                    day['resources'] = day['resources'][:3]
        
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get_detailed_day", response_model=DetailedDayPlan)
def get_detailed_day(request: DetailedDayRequest):
    print(f"Received detailed day request: topic='{request.topic}', day_topic='{request.day_topic}', day_number={request.day_number}")
    
    if not request.topic.strip() or not request.day_topic.strip():
        raise HTTPException(status_code=400, detail="Topic and day topic cannot be empty")
    
    if request.day_number < 1 or request.day_number > 7:
        raise HTTPException(status_code=400, detail="Day number must be between 1 and 7")
    
    try:
        llm = GeminiLLM()
        detailed_plan = llm.generate_detailed_day_plan(request.topic, request.day_topic, request.day_number)
        
        # Get comprehensive resources from Serper
        try:
            serper_resources = get_comprehensive_resources(request.topic, request.day_topic)
            detailed_plan['resources'] = serper_resources
        except Exception as serper_error:
            print(f"Serper API failed for detailed day: {serper_error}")
            # Use LLM-generated resources as fallback
            if 'resources' not in detailed_plan:
                detailed_plan['resources'] = []
        
        return detailed_plan
    except Exception as e:
        print(f"Error generating detailed day plan: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate detailed day plan: {str(e)}")
