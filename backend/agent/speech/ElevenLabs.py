import requests
import os
from typing import Optional
from pathlib import Path

class ElevenLabsAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the ElevenLabs API client.
        
        Args:
            api_key (str, optional): The API key for ElevenLabs. 
                                   If not provided, will look for ELEVEN_LABS_API_KEY in environment variables.
        """
        self.api_key = api_key or os.getenv('ELEVEN_LABS_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set as ELEVEN_LABS_API_KEY environment variable")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Default voice (Rachel)
        model_id: str = "eleven_monolingual_v1",
        output_path: Optional[str] = None
    ) -> bytes:
        """Convert text to speech using the specified voice.
        
        Args:
            text (str): The text to convert to speech
            voice_id (str): The ID of the voice to use
            model_id (str): The ID of the model to use
            output_path (str, optional): Path to save the audio file. If not provided, returns bytes.
        
        Returns:
            bytes: The audio data if output_path is not provided
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

        if output_path:
            Path(output_path).write_bytes(response.content)
            return None
        
        return response.content

    def get_voice_settings(self, voice_id: str) -> dict:
        """Get the settings for a specific voice."""
        response = requests.get(
            f"{self.base_url}/voices/{voice_id}/settings",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_user_info(self) -> dict:
        """Get information about the user's subscription and quota."""
        response = requests.get(
            f"{self.base_url}/user/subscription",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize the API client
    tts = ElevenLabsAPI()
    
    # Example 2: Convert text to speech and save to file
    text = """ 
Hey, I'm Anty
your personal daily planner for the magical city of Antwerp! ✨

Whether you're tired of visiting the same old spots or you're eager to discover hidden gems around the city, I'm here to craft a unique journey for you, one day at a time.

But first tell me a bit about your typical day, and I'll take care of the rest.

Let's make your everyday... a little more interesting!. 🚲✨

    """
    tts.text_to_speech(
        text=text,
        output_path="test_speech.mp3"
    )
    
    # Example 3: Get user subscription info
    user_info = tts.get_user_info()
    print("User info:", user_info)
