"""Main agent orchestration."""

import logging
from typing import Optional

from src.models.config import AppConfig
from src.services.gmail_service import GmailService
from src.services.calendar_service import CalendarService
from src.services.llm_service import LLMService
from src.utils.email_filter import filter_emails
from src.utils.storage import EmailStorage


class MeetingAgent:
    """Agent that processes emails and creates calendar meetings."""

    def __init__(self, config: AppConfig, logger: logging.Logger):
        """Initialize agent with configuration."""
        self.config = config
        self.logger = logger

        # Initialize services
        self.gmail_service = GmailService()
        self.calendar_service = CalendarService()
        self.llm_service = LLMService(config.llm)
        self.storage = EmailStorage(config.storage.database_path)

    def authenticate_services(self) -> None:
        """Authenticate all Google services."""
        self.logger.info("Authenticating Gmail service...")
        self.gmail_service.authenticate()

        self.logger.info("Authenticating Calendar service...")
        self.calendar_service.authenticate()

    def run(self) -> dict:
        """Execute one cycle of email processing."""
        self.logger.info("Starting agent run...")

        stats = {
            "emails_checked": 0,
            "emails_filtered": 0,
            "meetings_created": 0,
            "errors": 0,
        }

        try:
            # Fetch emails
            emails = self.gmail_service.get_emails(
                max_results=self.config.agent.max_emails_per_run
            )
            stats["emails_checked"] = len(emails)
            self.logger.info(f"Fetched {len(emails)} emails")

            # Filter emails
            filtered_emails = filter_emails(emails, self.config.gmail.filters)
            stats["emails_filtered"] = len(filtered_emails)
            self.logger.info(f"Filtered to {len(filtered_emails)} emails")

            # Track emails that didn't match filters
            filtered_ids = {email.id for email in filtered_emails}
            for email in emails:
                if email.id not in filtered_ids and not self.storage.is_processed(email.id):
                    self.storage.mark_as_processed(
                        email.id,
                        False,
                        email.subject,
                        email.sender,
                        "Did not match filter criteria (subject keywords)"
                    )

            # Process each email
            for email in filtered_emails:
                try:
                    self._process_email(email, stats)
                except Exception as e:
                    self.logger.error(f"Error processing email {email.id}: {e}")
                    stats["errors"] += 1

        except Exception as e:
            self.logger.error(f"Agent run failed: {e}")
            stats["errors"] += 1

        self.logger.info(f"Agent run completed: {stats}")
        return stats

    def _process_email(self, email, stats: dict) -> None:
        """Process a single email."""
        # Skip if already processed
        if self.storage.is_processed(email.id):
            self.logger.debug(f"Email {email.id} already processed, skipping")
            return

        self.logger.info(f"Processing email: {email.subject}")

        # Extract meeting info using LLM
        meeting = self.llm_service.extract_meeting_info(
            email.subject,
            email.get_plain_text_body(),
            self.config.calendar.default_duration_minutes,
        )

        if not meeting or not meeting.is_valid():
            self.logger.warning(f"Could not extract valid meeting from email {email.id}")
            self.storage.mark_as_processed(
                email.id,
                False,
                email.subject,
                email.sender,
                "Could not extract valid meeting information (missing date/time)"
            )
            return

        # Add email reference to description
        meeting.description = f"{meeting.description}\n\nSource: {email.subject}"

        # Create calendar event
        event_id = self.calendar_service.create_event(
            meeting,
            self.config.calendar.calendar_id
        )

        self.logger.info(f"Created calendar event {event_id} for meeting: {meeting.subject}")
        stats["meetings_created"] += 1

        # Mark as processed
        self.storage.mark_as_processed(
            email.id,
            True,
            email.subject,
            email.sender,
            None
        )

        # Mark email as read if configured
        if self.config.agent.mark_as_read_after_processing:
            self.gmail_service.mark_as_read(email.id)
