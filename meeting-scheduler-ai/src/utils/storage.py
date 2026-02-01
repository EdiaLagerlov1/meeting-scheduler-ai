"""Storage utilities for tracking processed emails."""

import sqlite3
from pathlib import Path
from datetime import datetime


class EmailStorage:
    """SQLite-based storage for tracking processed emails."""

    def __init__(self, db_path: str):
        """Initialize storage with database path."""
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self) -> None:
        """Create database and tables if they don't exist."""
        db_file = Path(self.db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_emails (
                email_id TEXT PRIMARY KEY,
                email_subject TEXT,
                email_sender TEXT,
                processed_at TEXT NOT NULL,
                meeting_created INTEGER NOT NULL,
                failure_reason TEXT
            )
        """)

        conn.commit()
        conn.close()

    def is_processed(self, email_id: str) -> bool:
        """Check if an email has already been processed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM processed_emails WHERE email_id = ?",
            (email_id,)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def mark_as_processed(
        self,
        email_id: str,
        meeting_created: bool,
        email_subject: str = "",
        email_sender: str = "",
        failure_reason: str = None
    ) -> None:
        """Mark an email as processed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO processed_emails
            (email_id, email_subject, email_sender, processed_at, meeting_created, failure_reason)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (email_id, email_subject, email_sender, datetime.utcnow().isoformat(),
             int(meeting_created), failure_reason)
        )

        conn.commit()
        conn.close()

    def get_stats(self) -> dict:
        """Get processing statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM processed_emails")
        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM processed_emails WHERE meeting_created = 1"
        )
        meetings_created = cursor.fetchone()[0]

        conn.close()

        return {
            "total_processed": total,
            "meetings_created": meetings_created,
        }
