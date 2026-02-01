"""Email data model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Email:
    """Represents an email message."""

    id: str
    sender: str
    subject: str
    body: str
    received_date: str
    labels: list[str]
    is_read: bool
    thread_id: Optional[str] = None

    def get_plain_text_body(self) -> str:
        """Extract plain text from body (HTML or plain text)."""
        # Simple implementation - can be enhanced for HTML parsing
        return self.body.strip()

    def matches_sender_filter(self, sender_filters: list[str]) -> bool:
        """Check if email sender matches any filter."""
        if not sender_filters:
            return True

        for filter_item in sender_filters:
            if filter_item.startswith("@"):
                # Domain match
                if filter_item in self.sender:
                    return True
            elif filter_item == self.sender:
                # Exact match
                return True
        return False

    def matches_subject_filter(self, keywords: list[str]) -> bool:
        """Check if subject contains any keyword."""
        if not keywords:
            return True

        subject_lower = self.subject.lower()
        return any(keyword.lower() in subject_lower for keyword in keywords)

    def matches_label_filter(self, label_filters: list[str]) -> bool:
        """Check if email has any required label."""
        if not label_filters:
            return True

        return any(label in self.labels for label in label_filters)

    def matches_read_filter(self, read_status: str) -> bool:
        """Check if email read status matches filter."""
        if read_status == "any":
            return True
        elif read_status == "read":
            return self.is_read
        elif read_status == "unread":
            return not self.is_read
        return True
