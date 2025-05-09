from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from pywebpush import webpush, WebPushException

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# These paths would be for persistent storage in production
SUBSCRIPTION_FILE = 'subscriptions.json'
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

# Load subscriptions on startup
load_subscriptions()

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

@app.route('/api/vapid-public-key', methods=['GET'])
def get_vapid_public_key():
    return jsonify({"publicKey": VAPID_PUBLIC_KEY})

@app.route('/api/notifications/subscribe', methods=['POST'])
def subscribe():
    try:
        subscription_info = request.json.get('subscription')
        if not subscription_info:
            return jsonify({"error": "No subscription data provided"}), 400
        
        # Check if subscription already exists
        if subscription_info not in subscriptions:
            subscriptions.append(subscription_info)
            save_subscriptions()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notifications/unsubscribe', methods=['POST'])
def unsubscribe():
    try:
        subscription_info = request.json.get('subscription')
        if not subscription_info:
            return jsonify({"error": "No subscription data provided"}), 400
        
        # Remove subscription if exists
        if subscription_info in subscriptions:
            subscriptions.remove(subscription_info)
            save_subscriptions()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/notifications/send', methods=['POST'])
def send_notification():
    try:
        data = request.json
        
        if not data or not data.get('title') or not data.get('body'):
            return jsonify({"error": "Missing required notification data"}), 400
        
        notification_data = {
            "title": data.get('title'),
            "body": data.get('body'),
            "url": data.get('url', '/'),
        }
        
        # Send to all subscriptions
        for subscription in subscriptions:
            try:
                webpush(
                    subscription_info=subscription,
                    data=json.dumps(notification_data),
                    vapid_private_key=VAPID_PRIVATE_KEY,
                    vapid_claims=VAPID_CLAIMS
                )
            except WebPushException as e:
                print(f"Web Push Exception: {e}")
                # Remove expired subscriptions
                if e.response and e.response.status_code == 410:
                    subscriptions.remove(subscription)
                    save_subscriptions()
            except Exception as e:
                print(f"Error sending notification: {e}")
        
        return jsonify({"success": True, "recipients": len(subscriptions)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add your API endpoints here

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 