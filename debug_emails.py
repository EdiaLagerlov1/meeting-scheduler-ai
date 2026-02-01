"""Debug script to see what emails are being fetched."""

from src.services.gmail_service import GmailService

# Initialize and authenticate
gmail = GmailService()
gmail.authenticate()

# Fetch emails
emails = gmail.get_emails(max_results=10)

print(f"\nFetched {len(emails)} emails:\n")
for i, email in enumerate(emails, 1):
    print(f"{i}. Subject: '{email.subject}'")
    print(f"   Sender: {email.sender}")
    print(f"   ID: {email.id}")
    print(f"   Labels: {email.labels}")
    print()
