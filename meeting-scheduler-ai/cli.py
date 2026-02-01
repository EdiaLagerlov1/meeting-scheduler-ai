"""Command-line interface for the meeting agent."""

import click
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

from src.models.config import AppConfig
from src.utils.config_loader import load_environment_variables, load_config
from src.utils.logger import setup_logger
from src.agent import MeetingAgent
from src.scheduler import AgentScheduler
from src.utils.storage import EmailStorage


@click.group()
def cli():
    """Gmail to Calendar Meeting Agent CLI."""
    pass


@cli.command()
@click.option(
    "--config",
    default="config.yaml",
    help="Path to configuration file",
)
def run(config: str):
    """Run the agent once manually."""
    load_environment_variables()
    app_config = load_config(config)
    logger = setup_logger(
        "meeting_agent",
        app_config.logging.file_path,
        app_config.logging.level,
    )

    try:
        agent = MeetingAgent(app_config, logger)
        agent.authenticate_services()
        stats = agent.run()

        click.echo("\n=== Agent Run Complete ===")
        click.echo(f"Emails checked: {stats['emails_checked']}")
        click.echo(f"Emails filtered: {stats['emails_filtered']}")
        click.echo(f"Meetings created: {stats['meetings_created']}")
        click.echo(f"Errors: {stats['errors']}")

    except Exception as e:
        logger.error(f"Agent run failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--config",
    default="config.yaml",
    help="Path to configuration file",
)
def schedule(config: str):
    """Start the agent scheduler for automatic execution."""
    load_environment_variables()
    app_config = load_config(config)
    logger = setup_logger(
        "meeting_agent",
        app_config.logging.file_path,
        app_config.logging.level,
    )

    try:
        scheduler = AgentScheduler(app_config, logger)
        click.echo(
            f"Starting scheduler (runs every {app_config.agent.schedule_interval_minutes} minutes)..."
        )
        click.echo("Press Ctrl+C to stop")
        scheduler.start()

    except Exception as e:
        logger.error(f"Scheduler failed: {e}")
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--config",
    default="config.yaml",
    help="Path to configuration file",
)
def stats(config: str):
    """Display processing statistics."""
    load_environment_variables()
    app_config = load_config(config)

    try:
        storage = EmailStorage(app_config.storage.database_path)
        stats_data = storage.get_stats()

        click.echo("\n=== Processing Statistics ===")
        click.echo(f"Total emails processed: {stats_data['total_processed']}")
        click.echo(f"Meetings created: {stats_data['meetings_created']}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--config",
    default="config.yaml",
    help="Path to configuration file",
)
@click.option(
    "--output",
    default="EMAIL_REPORT.md",
    help="Output file path for the report",
)
def report(config: str, output: str):
    """Generate markdown report of processed emails."""
    load_environment_variables()
    app_config = load_config(config)
    db_path = app_config.storage.database_path

    try:
        # Check if database exists
        if not Path(db_path).exists():
            click.echo(f"Database not found: {db_path}", err=True)
            sys.exit(1)

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
            click.echo("No processed emails found in database.")
            sys.exit(0)

        # Create markdown report
        report_lines = []
        report_lines.append("# Email Processing Report")
        report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append(f"Total Emails Processed: {len(rows)}\n")

        # Summary statistics
        meetings_created = sum(1 for row in rows if row[4] == 1)
        meetings_failed = len(rows) - meetings_created

        report_lines.append("## Summary\n")
        report_lines.append(f"- ✅ Meetings Created: {meetings_created}")
        report_lines.append(f"- ❌ Meetings Failed: {meetings_failed}\n")

        # Table
        report_lines.append("## Processed Emails\n")
        report_lines.append("| # | Subject | Sender | Processed At | Meeting Created | Reason |")
        report_lines.append("|---|---------|--------|--------------|-----------------|--------|")

        for idx, row in enumerate(rows, 1):
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

            report_lines.append(
                f"| {idx} | {email_subject} | {email_sender} | {processed_time} | {status} | {reason} |"
            )

        # Write to file
        report_content = "\n".join(report_lines)

        with open(output, 'w') as f:
            f.write(report_content)

        click.echo(f"✓ Report generated: {output}")
        click.echo(f"\nSummary:")
        click.echo(f"  Total processed: {len(rows)}")
        click.echo(f"  Meetings created: {meetings_created}")
        click.echo(f"  Failed to create: {meetings_failed}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
