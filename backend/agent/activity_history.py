import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ActivityHistory:
    def __init__(self):
        self.history_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'activity_history.json')
        self._ensure_history_file_exists()

    def _ensure_history_file_exists(self):
        """Ensure the history file exists and has the correct structure."""
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as f:
                json.dump({
                    "activities": [],
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)

    def add_activity(self, activity: Dict[str, Any], details: Dict[str, Any]) -> None:
        """Add a new activity to the history."""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)

            # Add timestamp to the activity
            activity_entry = {
                "activity": activity,
                "details": details,
                "timestamp": datetime.now().isoformat()
            }

            data["activities"].append(activity_entry)
            data["last_updated"] = datetime.now().isoformat()

            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error adding activity to history: {e}")
            raise

    def get_recent_activities(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent activities."""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
            
            # Return the most recent activities, limited by the specified number
            return data["activities"][-limit:]
        except Exception as e:
            print(f"Error getting recent activities: {e}")
            return []

    def get_activity_history(self) -> List[Dict[str, Any]]:
        """Get the complete activity history."""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
            return data["activities"]
        except Exception as e:
            print(f"Error getting activity history: {e}")
            return [] 