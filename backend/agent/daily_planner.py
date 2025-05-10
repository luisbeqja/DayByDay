from typing import Dict, List
from openai import AsyncOpenAI

from datetime import datetime
import os
from dotenv import load_dotenv
from .tools.weather import get_weather
from .tools.calendar_integration import get_today_events
latitude = 51.2194  # Example latitude for Antwerp
longitude = 4.4025  # Example longitude for Antwerp

load_dotenv()


AGENT_PROMPT = """
You are an AI assistant specialized in creating personalized daily activity recommendations 
for students in Antwerp. 

# [GUIDELINES]
You can use different tools and resources to get the information you need.
- You can use the antwerp map dataset and the antwerp events dataset to get the information you need.
- You can use a weather api to get the weather information you need.
- you can use an agent to get information about cultural spots in antwerp.

Focus on thinking aboutactivities that fit their schedule, interests, and preferred pace
Consider factors like:
- Student's daily schedule (classes, breaks)
- Preferred activity times
- Interest categories (culture, food, nature, shopping, entertainment)
- Desired activity pace (relaxed, moderate, active)
- Popular student locations and budget-friendly options in Antwerp

Your goal is based on the context create a daily plan for the user.
you dont have to give all the details, but you should give a general idea of the day.

# [OUTPUT FORMAT]
You MUST return the following JSON format:
{{
    "Morning": [
        "Activity 1",
        "Activity 2",
        "Activity 3"
    ],
    "Afternoon": [
        "Activity 1",
        "Activity 2",
        "Activity 3"
    ],
    "Evening": [
        "Activity 1",
        "Activity 2",
        "Activity 3"
    ]
}

# [EXAMPLE]
{
    "Morning": [
        "breakfast at 10:00",
        "go to the gym",
        "go to the university"
    ],
    "Afternoon": [
        "lunch at 12:00",
        "go to the park for studying",
        "relax with some music"
    ],
    "Evening": [
        "dinner at 20:00",
        "go to the cinema",
        "go to the bar"
    ]
}
"""


class AntyAIPlanner:
    def __init__(self):
        """Initialize the Anty AI agent with OpenAI configuration."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in environment variables")


        self.system_prompt = AGENT_PROMPT
        self.aclient = AsyncOpenAI(api_key=self.api_key)
        self.weather = get_weather(latitude, longitude)
        self.events = get_today_events()

    async def generate_recommendations(self, user_preferences: Dict) -> List[Dict]:
        """Generate personalized recommendations based on user preferences."""
        
        # Format the schedule times for better readability
        schedule = user_preferences['schedule']
        day_start = datetime.strptime(schedule['workStartTime'], '%H:%M').strftime('%I:%M %p')
        day_end = datetime.strptime(schedule['workEndTime'], '%H:%M').strftime('%I:%M %p')
        break_time = datetime.strptime(schedule['breakTime'], '%H:%M').strftime('%I:%M %p')
        
        # Construct the user prompt
        user_prompt = f"""
        these are the user preferences:

        Schedule:
        - Day starts at: {day_start}
        - Day ends at: {day_end}
        - Break time: {break_time} ({schedule['breakDuration']} minutes)
        
        Interests: {', '.join(user_preferences['interests'])}
        Preferred activity time: {user_preferences['preferredStartTime']} - {user_preferences['preferredEndTime']}
        Activity pace preference: {user_preferences['pace']}
        Weather: {self.weather}
        Events from the user's calendar: {self.events}
        # [OUTPUT FORMAT]
        You MUST return the following JSON format:
        {{
            "Morning": [
                "Activity 1",
                "Activity 2",
                "Activity 3"
            ],
            "Afternoon": [
                "Activity 1",
                "Activity 2",
                "Activity 3"
            ],
            "Evening": [
                "Activity 1",
                "Activity 2",
                "Activity 3"
            ]
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

    async def get_activity_details(self, activity_name: str) -> Dict:
        """Get detailed information about a specific activity."""
        try:
            response = await self.aclient.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable guide about activities and locations in Antwerp."},
                    {"role": "user", "content": f"Provide detailed information about {activity_name} in Antwerp, including:\n"
                                              "1. Historical significance\n"
                                              "2. What to expect\n"
                                              "3. Tips for students\n"
                                              "4. Nearby attractions\n"
                                              "Format the response as a JSON object."}
                ],
                temperature=0.7,
                max_tokens=500,
                response_format={ "type": "json_object" }
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error getting activity details: {e}")
            return {}


if __name__ == "__main__":
    import asyncio

    async def main():
        agent = AntyAIPlanner()
        user_preferences = {
            "schedule": {
                "workStartTime": "09:00",
                "workEndTime": "17:00",
                "breakTime": "12:00",
                "breakDuration": 30
            },
            "interests": ["culture", "food", "nature"],
            "preferredStartTime": "10:00",
            "preferredEndTime": "16:00",
            "pace": "moderate",
        }
        recommendations = await agent.generate_recommendations(user_preferences)
        print(recommendations)

    asyncio.run(main())
