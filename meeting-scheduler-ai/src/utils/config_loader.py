"""Configuration loading utilities."""

import os
import yaml
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

from src.models.config import (
    AppConfig,
    GmailConfig,
    GmailFilters,
    CalendarConfig,
    LLMConfig,
    AgentConfig,
    StorageConfig,
    LoggingConfig,
)


def load_environment_variables() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


def substitute_env_vars(value: Any) -> Any:
    """Replace ${VAR_NAME} with environment variable values."""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        var_name = value[2:-1]
        return os.getenv(var_name, value)
    return value


def load_config(config_path: str = "config.yaml") -> AppConfig:
    """Load and parse configuration file."""
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, "r") as f:
        config_data = yaml.safe_load(f)

    # Substitute environment variables
    config_data = _substitute_env_in_dict(config_data)

    # Parse configuration sections
    gmail_config = _parse_gmail_config(config_data.get("gmail", {}))
    calendar_config = _parse_calendar_config(config_data.get("calendar", {}))
    llm_config = _parse_llm_config(config_data.get("llm", {}))
    agent_config = _parse_agent_config(config_data.get("agent", {}))
    storage_config = _parse_storage_config(config_data.get("storage", {}))
    logging_config = _parse_logging_config(config_data.get("logging", {}))

    return AppConfig(
        gmail=gmail_config,
        calendar=calendar_config,
        llm=llm_config,
        agent=agent_config,
        storage=storage_config,
        logging=logging_config,
    )


def _substitute_env_in_dict(data: dict) -> dict:
    """Recursively substitute environment variables in dictionary."""
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = _substitute_env_in_dict(value)
        elif isinstance(value, list):
            result[key] = [substitute_env_vars(item) for item in value]
        else:
            result[key] = substitute_env_vars(value)
    return result


def _parse_gmail_config(data: dict) -> GmailConfig:
    """Parse Gmail configuration section."""
    filters_data = data.get("filters", {})
    filters = GmailFilters(
        senders=filters_data.get("senders", []),
        subject_keywords=filters_data.get("subject_keywords", []),
        labels=filters_data.get("labels", []),
        read_status=filters_data.get("read_status", "any"),
    )
    return GmailConfig(filters=filters)


def _parse_calendar_config(data: dict) -> CalendarConfig:
    """Parse Calendar configuration section."""
    return CalendarConfig(
        calendar_id=data.get("calendar_id", "primary"),
        default_duration_minutes=data.get("default_duration_minutes", 60),
    )


def _parse_llm_config(data: dict) -> LLMConfig:
    """Parse LLM configuration section."""
    return LLMConfig(
        provider=data.get("provider", "openai"),
        model=data.get("model", "gpt-4"),
        api_key=data.get("api_key", ""),
    )


def _parse_agent_config(data: dict) -> AgentConfig:
    """Parse Agent configuration section."""
    return AgentConfig(
        schedule_interval_minutes=data.get("schedule_interval_minutes", 30),
        max_emails_per_run=data.get("max_emails_per_run", 50),
        mark_as_read_after_processing=data.get("mark_as_read_after_processing", True),
    )


def _parse_storage_config(data: dict) -> StorageConfig:
    """Parse Storage configuration section."""
    return StorageConfig(database_path=data.get("database_path", "./data/processed_emails.db"))


def _parse_logging_config(data: dict) -> LoggingConfig:
    """Parse Logging configuration section."""
    return LoggingConfig(
        level=data.get("level", "INFO"),
        file_path=data.get("file_path", "./logs/agent.log"),
    )
