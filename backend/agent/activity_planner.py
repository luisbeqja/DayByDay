from typing import Dict, List
from openai import AsyncOpenAI

from datetime import datetime
import os
from dotenv import load_dotenv
from tools.weather import get_weather

latitude = 51.2194  # Example latitude for Antwerp
longitude = 4.4025  # Example longitude for Antwerp
load_dotenv()


AGENT_PROMPT = """
You are an AI assistant specialized in creating plan for an activity based.
you will recive as an input an activity name description like "visit the plantin moretus museum" or "go to the gym".
based on that you will create a plan for the activity.

# [GUIDELINES]
- you can choose a location from the antwerp map dataset.
- you have access to the weather api to get the weather information.
- remember that the user has a daily plan, so you should create an activity that fits the user's daily plan.

# [OUTPUT FORMAT]
You MUST return the following JSON format:

{{
    "activity_name": "Activity Name",
    "activity_description": "Activity Description",
    "text_to_speech": "Text to Speech description of the activity",
    "location_id": "Location ID"
}}


# [EXAMPLE]
{
    "activity_name": "breakfast",
    "activity_description": "have a breakfast at a local bakery",
    "text_to_speech": "Good morning! Anty here! It's 9:30 AM, and I know you've got classes this morning — but how about we start the day with something warm? I've found a cozy café nearby where you can grab breakfast before heading in.",
    "location_id": "1234567890"
}
"""


def load_antwerp_map_dataset():
    return """ 
    Quetzal - 0.012 km away
    Wasbar - 0.036 km away
    Chickpea - 0.061 km away
    Moochie - 0.064 km away
    De Plek - 0.089 km away
    """


class AntyAIActivityPlanner:
    def __init__(self):
        """Initialize the Anty AI agent with OpenAI configuration."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")


        self.system_prompt = AGENT_PROMPT
        self.aclient = AsyncOpenAI(api_key=self.api_key)
        self.weather = get_weather(latitude, longitude)
        self.current_time = datetime.now().strftime('%H:%M')
        self.antwerp_map_dataset = load_antwerp_map_dataset()
        
    async def generate_recommendations(self, activity_description: str) -> List[Dict]:
        """Generate personalized recommendations based on user preferences."""
        
        # Construct the user prompt
        user_prompt = f"""
        these are the user preferences:

        Activity description: {activity_description}
        Current time: {self.current_time}
        Current weather: {self.weather}
        Antwerp map dataset: {self.antwerp_map_dataset}
        
        # [OUTPUT FORMAT]
        You MUST return the following JSON format:

        {{
            "activity_name": "Activity Name",
            "activity_description": "Location Description",
            "text_to_speech": "Text to Speech description of the activity",
            "location_id": "Location ID"
        }}


        # [EXAMPLE]
        {{
            "activity_name": "breakfast",
            "activity_description": "",
            "text_to_speech": "Good morning! Anty here! It's 9:30 AM, and I know you've got classes this morning — but how about we start the day with something warm? I've found a cozy café nearby: ToiToiToi where you can grab breakfast before heading in.",
            "location_id": "1234567890"
        }}
        """

        try:
            response = await self.aclient.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                response_format={ "type": "json_object" }
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return {"recommendations": []}


if __name__ == "__main__":
    import asyncio
    planner = AntyAIActivityPlanner()
    print(asyncio.run(planner.generate_recommendations("Enjoy a coffee at a local cafe")))