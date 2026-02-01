"""Email filtering utilities."""

from src.models.email import Email
from src.models.config import GmailFilters


def filter_emails(emails: list[Email], filters: GmailFilters) -> list[Email]:
    """Filter emails based on configured criteria."""
    filtered = []

    for email in emails:
        if _matches_all_filters(email, filters):
            filtered.append(email)

    return filtered


def _matches_all_filters(email: Email, filters: GmailFilters) -> bool:
    """Check if email matches all filter criteria (AND logic)."""
    if not email.matches_sender_filter(filters.senders):
        return False

    if not email.matches_subject_filter(filters.subject_keywords):
        return False

    if not email.matches_label_filter(filters.labels):
        return False

    if not email.matches_read_filter(filters.read_status):
        return False

    return True
