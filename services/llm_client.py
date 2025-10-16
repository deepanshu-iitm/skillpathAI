import os
import json
import re
from typing import List, Dict
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiLLM:
    """Wrapper for Google Gemini model calls"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY in environment variables.")
        
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(model_name)

    def generate_learning_plan(self, topic: str) -> List[Dict]:
        """Generate a structured 7-day plan for the given topic using Gemini."""
        prompt = f"""
You are an expert learning designer.

Generate a structured **7-day learning plan** for the topic: "{topic}".

For each day, return a clear and valid JSON array with this structure:
[
  {{
    "day": "Day 1",
    "topic": "<subtopic title>",
    "mini_challenge": "<short hands-on task>",
    "reasoning": "<why this topic is on this day>",
    "resources": [
      {{ "type": "YouTube", "title": "<video title>", "url": "<link>" }},
      {{ "type": "Blog", "title": "<blog title>", "url": "<link>" }},
      {{ "type": "Article", "title": "<article title>", "url": "<link>" }}
    ]
  }},
  ...
]
Only return valid JSON — do not include explanations, markdown or text outside JSON.
        """

        try:
            response = self.client.generate_content(prompt)
            raw_output = response.text.strip()

            # Remove ```json or ``` and ``` wrappers if present
            raw_output = re.sub(r"^```(json)?", "", raw_output)
            raw_output = re.sub(r"```$", "", raw_output)
            raw_output = raw_output.strip()

            # Extract first valid JSON array using regex
            match = re.search(r"\[.*\]", raw_output, re.DOTALL)
            if not match:
                raise ValueError("No JSON array found in Gemini output.")
            
            json_text = match.group(0).strip()

            # Parse safely 
            plan = json.loads(json_text)
            return plan

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON: {e}\nRaw output:\n{raw_output[:1000]}")
        except Exception as e:
            raise RuntimeError(f"Gemini failed to generate a learning plan: {e}")
