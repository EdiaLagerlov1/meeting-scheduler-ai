"""Google Calendar API service."""

import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from src.models.meeting import Meeting

SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalendarService:
    """Service for interacting with Google Calendar API."""

    def __init__(self, credentials_file: str = "credentials.json"):
        """Initialize Calendar service with OAuth credentials."""
        self.credentials_file = credentials_file
        self.token_file = "calendar_token.pickle"
        self.service = None

    def authenticate(self) -> None:
        """Authenticate with Google Calendar API using OAuth2."""
        creds = None

        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_file, "wb") as token:
                pickle.dump(creds, token)

        self.service = build("calendar", "v3", credentials=creds)

    def create_event(self, meeting: Meeting, calendar_id: str = "primary") -> str:
        """Create a calendar event from a Meeting object."""
        if not self.service:
            raise RuntimeError("Service not authenticated. Call authenticate() first.")

        if not meeting.is_valid():
            raise ValueError("Invalid meeting data")

        event_body = meeting.to_calendar_event()

        event = self.service.events().insert(
            calendarId=calendar_id,
            body=event_body
        ).execute()

        return event.get("id", "")

    def event_exists(self, meeting: Meeting, calendar_id: str = "primary") -> bool:
        """Check if a similar event already exists."""
        if not self.service:
            raise RuntimeError("Service not authenticated.")

        # Search for events with same summary and start time
        time_min = meeting.start_datetime.isoformat()
        time_max = meeting.end_datetime.isoformat()

        events = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            q=meeting.subject,
            singleEvents=True,
        ).execute()

        return len(events.get("items", [])) > 0
