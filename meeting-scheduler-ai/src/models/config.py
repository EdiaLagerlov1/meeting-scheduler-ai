"""Configuration data model."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GmailFilters:
    """Gmail filtering configuration."""

    senders: list[str] = field(default_factory=list)
    subject_keywords: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    read_status: str = "any"


@dataclass
class GmailConfig:
    """Gmail service configuration."""

    filters: GmailFilters = field(default_factory=GmailFilters)


@dataclass
class CalendarConfig:
    """Calendar service configuration."""

    calendar_id: str = "primary"
    default_duration_minutes: int = 60


@dataclass
class LLMConfig:
    """LLM service configuration."""

    provider: str = "openai"
    model: str = "gpt-4"
    api_key: str = ""


@dataclass
class AgentConfig:
    """Agent runtime configuration."""

    schedule_interval_minutes: int = 30
    max_emails_per_run: int = 50
    mark_as_read_after_processing: bool = True


@dataclass
class StorageConfig:
    """Storage configuration."""

    database_path: str = "./data/processed_emails.db"


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    file_path: str = "./logs/agent.log"


@dataclass
class AppConfig:
    """Application configuration."""

    gmail: GmailConfig = field(default_factory=GmailConfig)
    calendar: CalendarConfig = field(default_factory=CalendarConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
