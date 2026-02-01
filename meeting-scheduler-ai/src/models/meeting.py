"""Meeting data model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Meeting:
    """Represents a meeting to be added to calendar."""

    subject: str
    start_datetime: datetime
    end_datetime: datetime
    description: str
    location: Optional[str] = None
    attendees: Optional[list[str]] = None

    def to_calendar_event(self) -> dict:
        """Convert to Google Calendar event format."""
        event = {
            "summary": self.subject,
            "description": self.description,
            "start": {
                "dateTime": self.start_datetime.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": self.end_datetime.isoformat(),
                "timeZone": "UTC",
            },
        }

        if self.location:
            event["location"] = self.location

        if self.attendees:
            event["attendees"] = [{"email": email} for email in self.attendees]

        return event

    def is_valid(self) -> bool:
        """Validate meeting has required fields."""
        if not self.subject or not self.subject.strip():
            return False
        if not self.start_datetime or not self.end_datetime:
            return False
        if self.end_datetime <= self.start_datetime:
            return False
        return True
