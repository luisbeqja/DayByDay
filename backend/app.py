from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from pywebpush import webpush, WebPushException
from agent.speech.ElevenLabs import ElevenLabsAPI
from agent.orchestrator import OrchestratorAgent, TaskType
from io import BytesIO
from asgiref.wsgi import WsgiToAsgi

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the orchestrator
orchestrator = OrchestratorAgent()

# These paths would be for persistent storage in production
SUBSCRIPTION_FILE = 'subscriptions.json'
PREFERENCES_FILE = 'user_preferences.json'
VAPID_PRIVATE_KEY_FILE = 'private_key.pem'

# VAPID keys should be generated and stored securely
# For simplicity, we're using placeholder values
VAPID_PRIVATE_KEY = os.getenv('VAPID_PRIVATE_KEY', 'your-private-key')
VAPID_PUBLIC_KEY = os.getenv('VAPID_PUBLIC_KEY', 'your-public-key')
VAPID_CLAIMS = {
    "sub": "mailto:your-email@example.com"
}

# Simple in-memory storage for demo purposes
subscriptions = []

# Load existing subscriptions if file exists
def load_subscriptions():
    global subscriptions
    try:
        if os.path.exists(SUBSCRIPTION_FILE):
            with open(SUBSCRIPTION_FILE, 'r') as f:
                subscriptions = json.load(f)
    except Exception as e:
        print(f"Error loading subscriptions: {e}")

# Save subscriptions to file
def save_subscriptions():
    try:
        with open(SUBSCRIPTION_FILE, 'w') as f:
            json.dump(subscriptions, f)
    except Exception as e:
        print(f"Error saving subscriptions: {e}")

# Load existing preferences if file exists
def load_preferences():
    try:
        if os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading preferences: {e}")
        return {}

# Save preferences to file
def save_preferences(preferences):
    try:
        with open(PREFERENCES_FILE, 'w') as f:
            json.dump(preferences, f)
    except Exception as e:
        print(f"Error saving preferences: {e}")

# Load subscriptions and preferences on startup
load_subscriptions()
user_preferences = load_preferences()

# Initialize ElevenLabs API with development mode
tts = ElevenLabsAPI(dev_mode=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is running"})

@app.route('/api/info', methods=['GET'])
def get_info():
    return jsonify({
        "app": "Vue PWA with Flask Backend",
        "version": "1.0.0",
        "description": "A boilerplate for building Progressive Web Apps with Vue and Flask"
    })

@app.route('/api/welcome-audio', methods=['GET'])
def get_welcome_audio():
    try:
        welcome_text = """
Hey there, I'm Anty!
your personal daily planner for the magical city of Antwerp! ✨

Whether you're tired of visiting the same old spots or you're eager to discover hidden gems around the city, I'm here to craft a unique journey for you, one day at a time.

But first tell me a bit about your typical day, and I'll take care of the rest.

Let's make your everyday... a little more interesting. 🚲✨
        """
        
        # Generate audio
        audio_data = tts.text_to_speech(text=welcome_text)
        
        # Create a BytesIO object
        audio_buffer = BytesIO(audio_data)
        audio_buffer.seek(0)
        
        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='welcome.mp3'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preferences', methods=['POST'])
async def save_user_preferences():
    try:
        preferences = request.json
        if not preferences:
            return jsonify({"error": "No preferences data provided"}), 400
            
        # Validate required fields
        required_fields = ['occupation', 'schedule', 'interests', 'pace', 'preferredStartTime', 'preferredEndTime']
        for field in required_fields:
            if field not in preferences:
                return jsonify({"error": f"Missing required field: {field}"}), 400
                
        # Validate schedule fields
        schedule_fields = ['workStartTime', 'workEndTime', 'breakTime', 'breakDuration']
        for field in schedule_fields:
            if field not in preferences['schedule']:
                return jsonify({"error": f"Missing required schedule field: {field}"}), 400
            
        # Save preferences
        save_preferences(preferences)
        
        # Get daily plan using the orchestrator
        daily_planner_result = await orchestrator.delegate_task(
            TaskType.DAILY_PLANNER,
            user_preferences=preferences
        )
        
        if daily_planner_result['status'] == 'error':
            return jsonify({"error": daily_planner_result['error']}), 500
            
        return jsonify({
            "success": True,
            "daily_plan": daily_planner_result['result']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/preferences', methods=['GET'])
def get_user_preferences():
    return jsonify(user_preferences)


@app.route('/api/agent/get-activity', methods=['GET'])
async def get_activity():
    daily_planner_result = await orchestrator.delegate_task(
            TaskType.DAILY_PLANNER,
            user_preferences=user_preferences
        )
    print(daily_planner_result)
    activity_planner_result = await orchestrator.handle_activity_planning(daily_planner_result)

    return jsonify(activity_planner_result)

# Convert Flask app to ASGI
app = WsgiToAsgi(app)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 