"""Gmail API service."""

import base64
from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

from src.models.email import Email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.modify"]


class GmailService:
    """Service for interacting with Gmail API."""

    def __init__(self, credentials_file: str = "credentials.json"):
        """Initialize Gmail service with OAuth credentials."""
        self.credentials_file = credentials_file
        self.token_file = "gmail_token.pickle"
        self.service = None

    def authenticate(self) -> None:
        """Authenticate with Gmail API using OAuth2."""
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

        self.service = build("gmail", "v1", credentials=creds)

    def get_emails(self, max_results: int = 50) -> list[Email]:
        """Fetch emails from Gmail."""
        if not self.service:
            raise RuntimeError("Service not authenticated. Call authenticate() first.")

        results = self.service.users().messages().list(
            userId="me", maxResults=max_results
        ).execute()

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            email = self._fetch_email_details(msg["id"])
            if email:
                emails.append(email)

        return emails

    def _fetch_email_details(self, msg_id: str) -> Optional[Email]:
        """Fetch full details for a specific email."""
        msg = self.service.users().messages().get(
            userId="me", id=msg_id, format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}

        sender = headers.get("From", "")
        subject = headers.get("Subject", "")
        date = headers.get("Date", "")

        body = self._extract_body(msg["payload"])
        labels = msg.get("labelIds", [])
        is_read = "UNREAD" not in labels

        return Email(
            id=msg_id,
            sender=sender,
            subject=subject,
            body=body,
            received_date=date,
            labels=labels,
            is_read=is_read,
            thread_id=msg.get("threadId"),
        )

    def _extract_body(self, payload: dict) -> str:
        """Extract email body from payload."""
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    return base64.urlsafe_b64decode(data).decode("utf-8")

        if "body" in payload and "data" in payload["body"]:
            data = payload["body"]["data"]
            return base64.urlsafe_b64decode(data).decode("utf-8")

        return ""

    def mark_as_read(self, email_id: str) -> None:
        """Mark an email as read."""
        if not self.service:
            raise RuntimeError("Service not authenticated.")

        self.service.users().messages().modify(
            userId="me",
            id=email_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()
