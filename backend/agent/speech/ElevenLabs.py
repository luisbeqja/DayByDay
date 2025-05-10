import requests
import os
from typing import Optional
from pathlib import Path
import base64

class ElevenLabsAPI:
    def __init__(self, api_key: Optional[str] = None, dev_mode: bool = False):
        """Initialize the ElevenLabs API client.
        
        Args:
            api_key (str, optional): The API key for ElevenLabs. 
                                   If not provided, will look for ELEVEN_LABS_API_KEY in environment variables.
            dev_mode (bool): If True, uses mock responses instead of making API calls.
        """
        self.dev_mode = dev_mode
        if not dev_mode:
            self.api_key = api_key or os.getenv('ELEVEN_LABS_API_KEY')
            if not self.api_key:
                raise ValueError("API key must be provided or set as ELEVEN_LABS_API_KEY environment variable")
            
            self.base_url = "https://api.elevenlabs.io/v1"
            self.headers = {
                "Accept": "application/json",
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }

    def _get_mock_audio(self) -> bytes:
        """Generate a mock audio response for development mode.
        Returns a short silent MP3 file."""
        # This is a base64 encoded 1-second silent MP3 file
        silent_mp3_base64 = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//tQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAADwAD///////////////////////////////////////////8AAAA8TEFNRTMuMTAwAQAAAAAAAAAAABSAJAJAQgAAgAAAA8D1f0bYAAAAAAAAAAAAAAAAAAAA"
        return base64.b64decode(silent_mp3_base64)

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "pNInz6obpgDQGcFmaJgB",  # Changed to Adam (more energetic voice)
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
        if self.dev_mode:
            print(f"[DEV MODE] Text to speech: {text}")
            audio_data = self._get_mock_audio()
            if output_path:
                Path(output_path).write_bytes(audio_data)
                return None
            return audio_data

        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.35,  # Lower stability for more expressiveness
                "similarity_boost": 0.75,  # Higher similarity boost for more character
                "style": 0.85,  # Added style parameter for more excitement
                "use_speaker_boost": True  # Enable speaker boost for clearer voice
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
        if self.dev_mode:
            print(f"[DEV MODE] Getting voice settings for: {voice_id}")
            return {
                "stability": 0.35,
                "similarity_boost": 0.75,
                "style": 0.85,
                "use_speaker_boost": True
            }

        response = requests.get(
            f"{self.base_url}/voices/{voice_id}/settings",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_user_info(self) -> dict:
        """Get information about the user's subscription and quota."""
        if self.dev_mode:
            print("[DEV MODE] Getting user info")
            return {
                "character_count": 0,
                "character_limit": 10000,
                "can_extend_character_limit": True,
                "available_models": ["eleven_monolingual_v1"],
                "subscription": {
                    "tier": "free",
                    "character_count": 0,
                    "character_limit": 10000,
                    "can_extend_character_limit": True,
                    "available_models": ["eleven_monolingual_v1"]
                }
            }

        response = requests.get(
            f"{self.base_url}/user/subscription",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
