import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

# OAuth 2.0 Scopes (calendar read or read/write)
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authenticate_calendar():
    creds = None

    # Create the flow using client ID/secret from .env
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],  # noqa
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",  # noqa
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )

    # Open local server to get auth code
    creds = flow.run_local_server(port=0)

    return creds


def get_today_events():
    creds = authenticate_calendar()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)  # Start of today  # noqa
    today_end = today_start + timedelta(days=1)  # End of today (24 hours later)  # noqa

    events_result = service.events().list(
        calendarId='primary',
        timeMin=today_start.isoformat() + 'Z',
        timeMax=today_end.isoformat() + 'Z',
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events_result.get('items', [])


def main():
    events = get_today_events()
    if not events:
        print("No events found for today.")
    else:
        print("Your plans for today:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"- {event['summary']} at {start}")


if __name__ == '__main__':
    main()
