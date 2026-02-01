"""Script to send test meeting emails via Gmail API."""

import pickle
import os.path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'
]


def authenticate():
    """Authenticate with Gmail API."""
    creds = None
    token_file = "send_email_token.pickle"

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def create_message(to, subject, body):
    """Create email message."""
    message = EmailMessage()
    message['To'] = to
    message['Subject'] = subject
    message.set_content(body)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


def send_email(service, user_email, subject, body):
    """Send email."""
    try:
        message = create_message(user_email, subject, body)
        sent = service.users().messages().send(
            userId='me', body=message
        ).execute()
        print(f"✓ Sent: {subject}")
        return sent
    except Exception as e:
        print(f"✗ Error sending {subject}: {e}")
        return None


def main():
    """Send 3 test meeting emails."""
    print("Authenticating with Gmail...")
    service = authenticate()

    # Get user's email address
    profile = service.users().getProfile(userId='me').execute()
    user_email = profile['emailAddress']
    print(f"Sending test emails to: {user_email}\n")

    # Calculate dates for this week only
    tomorrow = datetime.now() + timedelta(days=1)
    day_after_tomorrow = datetime.now() + timedelta(days=2)
    in_three_days = datetime.now() + timedelta(days=3)

    # Email 1: Team Meeting
    subject1 = "Team Meeting - Q1 Planning"
    body1 = f"""Hi Team,

Let's schedule our Q1 planning meeting.

Date: {tomorrow.strftime('%B %d, %Y')}
Time: 2:00 PM
Duration: 90 minutes
Location: Conference Room B

Agenda:
- Review Q4 results
- Set Q1 goals
- Resource allocation

See you there!
"""

    # Email 2: Client Sync
    subject2 = "Sync appointment with Client ABC"
    body2 = f"""Hello,

Scheduled sync meeting with Client ABC.

When: {day_after_tomorrow.strftime('%Y-%m-%d')} at 10:30 AM
Duration: 1 hour
Where: Zoom (link will be sent separately)

Topics:
- Project status update
- Timeline review
- Next milestones

Thanks!
"""

    # Email 3: 1-on-1 Meeting
    subject3 = "1-on-1 Meeting Scheduled"
    body3 = f"""Hi,

Your 1-on-1 meeting has been scheduled.

Date: {in_three_days.strftime('%B %d, %Y')}
Time: 3:30 PM
Duration: 30 minutes
Location: My Office

We'll discuss your progress and any concerns.

Best regards
"""

    # Send emails
    print("Sending test emails...\n")
    send_email(service, user_email, subject1, body1)
    send_email(service, user_email, subject2, body2)
    send_email(service, user_email, subject3, body3)

    print("\n✓ All test emails sent!")
    print("\nRun 'python cli.py run' to process them.")


if __name__ == '__main__':
    main()
