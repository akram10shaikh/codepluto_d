from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime



def get_calendar_service():
    credentials = Credentials.from_service_account_file(
        'credentials.json',  # ← Update with your correct path
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    return build('calendar', 'v3', credentials=credentials)

def create_google_meet_event(title, description, start_time, end_time, attendees=[]):
    service = get_calendar_service()

    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in attendees if email],
        'conferenceData': {
            'createRequest': {
                'requestId': f"meet_{datetime.datetime.now().timestamp()}"
            }
        }
    }

    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    return event
