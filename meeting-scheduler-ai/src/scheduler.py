"""Scheduler for automatic agent execution."""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.models.config import AppConfig
from src.agent import MeetingAgent


class AgentScheduler:
    """Scheduler for running the agent at regular intervals."""

    def __init__(self, config: AppConfig, logger: logging.Logger):
        """Initialize scheduler with configuration."""
        self.config = config
        self.logger = logger
        self.agent = MeetingAgent(config, logger)
        self.scheduler = BlockingScheduler()

    def start(self) -> None:
        """Start the scheduler."""
        # Authenticate services once at startup
        self.logger.info("Authenticating services...")
        self.agent.authenticate_services()

        # Run once immediately
        self.logger.info("Running initial agent cycle...")
        self.agent.run()

        # Schedule periodic runs
        interval_minutes = self.config.agent.schedule_interval_minutes
        self.logger.info(f"Scheduling agent to run every {interval_minutes} minutes")

        self.scheduler.add_job(
            self.agent.run,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id="meeting_agent_job",
            name="Meeting Agent Periodic Run",
            replace_existing=True,
        )

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("Scheduler stopped")
            self.scheduler.shutdown()
