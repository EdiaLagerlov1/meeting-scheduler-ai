"""Generate a markdown report of processed emails."""

import sqlite3
from pathlib import Path
from datetime import datetime


def generate_report(db_path: str, output_file: str = "EMAIL_REPORT.md"):
    """Generate markdown report from processed emails database."""

    # Check if database exists
    if not Path(db_path).exists():
        print(f"Database not found: {db_path}")
        return

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all processed emails
    cursor.execute("""
        SELECT email_id, email_subject, email_sender, processed_at, meeting_created, failure_reason
        FROM processed_emails
        ORDER BY processed_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No processed emails found in database.")
        return

    # Create markdown report
    report = []
    report.append("# Email Processing Report")
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"Total Emails Processed: {len(rows)}\n")

    # Summary statistics
    meetings_created = sum(1 for row in rows if row[2] == 1)
    meetings_failed = len(rows) - meetings_created

    report.append("## Summary\n")
    report.append(f"- ✅ Meetings Created: {meetings_created}")
    report.append(f"- ❌ Meetings Failed: {meetings_failed}\n")

    # Table
    report.append("## Processed Emails\n")
    report.append("| # | Subject | Sender | Processed At | Meeting Created | Reason |")
    report.append("|---|---------|--------|--------------|-----------------|--------|")

    for idx, row in enumerate(rows, 1):
        email_id = row[0]
        email_subject = row[1] or "N/A"
        email_sender = row[2] or "N/A"
        processed_at = row[3]
        meeting_created = row[4]
        failure_reason = row[5]

        # Format datetime
        try:
            dt = datetime.fromisoformat(processed_at)
            processed_time = dt.strftime('%Y-%m-%d %H:%M')
        except:
            processed_time = processed_at

        # Truncate subject if too long
        if len(email_subject) > 40:
            email_subject = email_subject[:37] + "..."

        # Truncate sender if too long
        if len(email_sender) > 30:
            email_sender = email_sender[:27] + "..."

        # Status and reason
        if meeting_created == 1:
            status = "✅ Yes"
            reason = "Successfully created calendar event"
        else:
            status = "❌ No"
            reason = failure_reason or "Could not extract valid meeting information"

        report.append(
            f"| {idx} | {email_subject} | {email_sender} | {processed_time} | {status} | {reason} |"
        )

    # Write to file
    report_content = "\n".join(report)

    with open(output_file, 'w') as f:
        f.write(report_content)

    print(f"✓ Report generated: {output_file}")
    print(f"\nSummary:")
    print(f"  Total processed: {len(rows)}")
    print(f"  Meetings created: {meetings_created}")
    print(f"  Failed to create: {meetings_failed}")


if __name__ == '__main__':
    generate_report("./data/processed_emails.db")
