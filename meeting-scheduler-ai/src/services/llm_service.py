"""LLM service for extracting meeting information."""

import json
from datetime import datetime, timedelta
from typing import Optional

from src.models.meeting import Meeting
from src.models.config import LLMConfig


class LLMService:
    """Service for interacting with LLM APIs."""

    def __init__(self, config: LLMConfig):
        """Initialize LLM service with configuration."""
        self.config = config
        self.client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the appropriate LLM client based on provider."""
        if self.config.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=self.config.api_key)
        elif self.config.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.config.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.config.provider}")

    def extract_meeting_info(
        self,
        email_subject: str,
        email_body: str,
        default_duration: int = 60
    ) -> Optional[Meeting]:
        """Extract meeting information from email using LLM."""
        prompt = self._build_extraction_prompt(email_subject, email_body)

        if self.config.provider == "openai":
            response = self._call_openai(prompt)
        elif self.config.provider == "anthropic":
            response = self._call_anthropic(prompt)
        else:
            return None

        return self._parse_llm_response(response, default_duration)

    def _build_extraction_prompt(self, subject: str, body: str) -> str:
        """Build prompt for LLM to extract meeting details."""
        return f"""Extract meeting information from the following email.
Return a JSON object with these fields:
- subject: Meeting title/subject
- date: Meeting date in ISO format (YYYY-MM-DD)
- time: Meeting time in 24h format (HH:MM)
- duration_minutes: Duration in minutes (if specified)
- description: Brief meeting description
- location: Physical or virtual location (if specified)
- attendees: List of email addresses (if specified)

If any information is not found, omit that field from the JSON.

Email Subject: {subject}

Email Body:
{body}

Return ONLY the JSON object, no additional text.
"""

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "You are a meeting information extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API."""
        response = self.client.messages.create(
            model=self.config.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        return response.content[0].text

    def _parse_llm_response(
        self,
        response: str,
        default_duration: int
    ) -> Optional[Meeting]:
        """Parse LLM response and create Meeting object."""
        try:
            # Extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            json_str = response[json_start:json_end]

            data = json.loads(json_str)

            # Parse datetime
            date_str = data.get("date")
            time_str = data.get("time", "09:00")

            if not date_str:
                return None

            start_datetime = datetime.fromisoformat(f"{date_str}T{time_str}")
            duration = data.get("duration_minutes", default_duration)
            end_datetime = start_datetime + timedelta(minutes=duration)

            return Meeting(
                subject=data.get("subject", "Meeting"),
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                description=data.get("description", ""),
                location=data.get("location"),
                attendees=data.get("attendees"),
            )
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            return None
