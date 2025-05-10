from typing import Dict, List, Any
from openai import AsyncOpenAI

from datetime import datetime
import os
from dotenv import load_dotenv
from .tools.weather import get_weather
import json
from .tools.geosorting import main
# Load environment variables
load_dotenv()

# Constants
latitude = 51.2194  # Example latitude for Antwerp
longitude = 4.4024  # Example longitude for Antwerp

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
    
# Load amenities from JSON file
def load_amenities() -> List[str]:
    json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'possible_keys', 'amenitys.json')
    with open(json_path, 'r') as f:
        return json.load(f)

AMENITIES = load_amenities()
    
    
    

class AntyAIActivityPlanner:
    def __init__(self):
        """Initialize the Anty AI agent with OpenAI configuration."""
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.weather = get_weather(latitude, longitude)
        self.amenities = AMENITIES
        self.system_prompt = AGENT_PROMPT
        self.current_time = datetime.now().strftime('%H:%M')
        self.antwerp_map_dataset = load_antwerp_map_dataset()
    
    async def select_dataset_to_use(self, activity_description: str):
        prompt = f"""
        this are all the possible datasets that you can use:
        {self.amenities}
        based on the activity description, select the most relevant dataset to use.
        activity description: {activity_description}
        # [OUTPUT FORMAT]
        You MUST return the following JSON format:
        {{
            "dataset": "Dataset Name"
        }}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    
    async def generate_recommendations(self, activity_description: str) -> List[Dict]:
        """Generate personalized recommendations based on user preferences."""
        
        try:
            # Get the dataset selection
            dataset_result = await self.select_dataset_to_use(activity_description)
            print("Selected dataset:", dataset_result)
            
            # Update the map dataset based on the selected dataset
            self.antwerp_map_dataset = main(dataset_result['dataset'])
            print("Updated map dataset:", self.antwerp_map_dataset)
            
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

            response = await self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000,
                response_format={ "type": "json_object" }
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return {
                "result": None,
                "status": "error",
                "error": str(e)
            }


if __name__ == "__main__":
    import asyncio
    planner = AntyAIActivityPlanner()
    print(asyncio.run(planner.select_dataset_to_use("Enjoy a coffee at a local cafe")))