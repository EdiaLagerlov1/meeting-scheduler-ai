# Product Requirements Document: Gmail to Calendar Meeting Agent

## Overview
An automated agent that monitors Gmail for emails matching predefined criteria and automatically creates Google Calendar meetings by extracting meeting details using an LLM.

## Objectives
- Automate the process of creating calendar meetings from qualifying emails
- Reduce manual effort in scheduling meetings from email invitations
- Provide flexible filtering to target specific types of emails
- Enable both automatic and manual operation modes
- Track and report on all processed emails with detailed analytics

## Core Features

### 1. Email Monitoring & Filtering
**Requirements:**
- Connect to Gmail via Gmail API with OAuth 2.0 authentication
- Filter emails based on configurable criteria:
  - Sender email address (exact match or domain)
  - Keywords in subject line
  - Gmail labels
  - Read/unread status
- Process only emails that match ALL specified criteria (AND logic)
- Track ALL checked emails (including those that don't match filters)
- Store email metadata: subject, sender, processing timestamp, status, failure reason

### 2. Meeting Information Extraction
**Requirements:**
- Use LLM API (configurable provider: OpenAI or Anthropic) to extract meeting details from email content
- Extract the following fields:
  - Meeting subject/title
  - Date and time
  - Duration (if specified)
  - Description/agenda
  - Location (physical or virtual meeting link)
  - Attendees (if applicable)
- Handle various email formats (plain text, HTML)
- Parse common date/time formats and natural language expressions
- Track extraction failures with detailed reasons

### 3. Calendar Integration
**Requirements:**
- Connect to Google Calendar API with OAuth 2.0 authentication
- Create calendar events with extracted information:
  - Event title (from meeting subject)
  - Start date/time
  - End date/time (calculated from duration or default to 60 minutes)
  - Description (from email content + original email reference)
  - Location (if available)
- Add attendees to the calendar event if email addresses are detected
- Set default calendar or allow configuration of target calendar
- Prevent duplicate event creation for the same email

### 4. Agent Execution Modes
**Requirements:**
- **Automatic Mode:** Run every 30 minutes via APScheduler
- **Manual Mode:** Allow on-demand execution via command-line interface
- Provide detailed logging for each execution cycle showing:
  - Number of emails checked
  - Number of emails filtered
  - Number of meetings created
  - Any errors or warnings
- Support graceful error handling and recovery

### 5. Configuration Management
**Requirements:**
- Support YAML configuration file with following settings:
  ```yaml
  gmail:
    filters:
      senders: []  # Empty array = match all
      subject_keywords: ["meeting", "appointment", "sync"]
      labels: []  # Empty array = match all
      read_status: "any"  # Options: unread, read, any

  calendar:
    calendar_id: "primary"
    default_duration_minutes: 60

  llm:
    provider: "openai"  # Options: openai, anthropic
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-3.5-turbo"  # or "claude-3-sonnet-20240229"

  agent:
    schedule_interval_minutes: 30
    max_emails_per_run: 50
    mark_as_read_after_processing: true

  storage:
    database_path: "./data/processed_emails.db"

  logging:
    level: "INFO"
    file_path: "./logs/agent.log"
  ```
- Validate configuration on startup
- Support environment variables for sensitive data (API keys)
- Load environment variables from .env file

### 6. Reporting & Analytics
**Requirements:**
- Generate comprehensive markdown reports of processed emails
- Report includes:
  - Total emails checked vs. filtered vs. meetings created
  - Detailed table with: Email subject, Sender, Timestamp, Status, Reason
  - Success/failure breakdown with statistics
- Export reports via CLI command
- Store detailed failure reasons for troubleshooting

### 7. Testing & Development Tools
**Requirements:**
- Test email generator script to create sample meeting emails
- Debug utilities to inspect fetched emails
- Ability to clear database for testing
- Sample test emails with proper meeting information

## Technical Architecture

### Components
1. **Gmail Service** (`src/services/gmail_service.py`): Handle Gmail API authentication and email fetching
2. **Email Processor** (`src/utils/email_filter.py`): Apply filters and extract email content
3. **LLM Service** (`src/services/llm_service.py`): Send prompts to LLM API and parse responses
4. **Calendar Service** (`src/services/calendar_service.py`): Handle Google Calendar API authentication and event creation
5. **Scheduler** (`src/scheduler.py`): Manage automatic execution intervals using APScheduler
6. **CLI Interface** (`cli.py`): Provide manual execution, stats, and report generation
7. **Storage** (`src/utils/storage.py`): Track processed emails with metadata in SQLite database
8. **Agent Orchestrator** (`src/agent.py`): Coordinate all services and execution flow

### Database Schema
```sql
CREATE TABLE processed_emails (
    email_id TEXT PRIMARY KEY,
    email_subject TEXT,
    email_sender TEXT,
    processed_at TEXT NOT NULL,
    meeting_created INTEGER NOT NULL,
    failure_reason TEXT
)
```

### Technology Stack
- **Language:** Python 3.13+
- **Gmail API:** google-api-python-client==2.111.0
- **Calendar API:** google-api-python-client==2.111.0
- **LLM Integration:** openai==2.16.0, anthropic==0.77.0
- **Scheduling:** APScheduler==3.10.4
- **Configuration:** PyYAML==6.0.1, python-dotenv==1.0.0
- **CLI:** click==8.1.7
- **Storage:** SQLite3 (built-in)
- **Logging:** Python logging module (built-in)

### File Structure
```
set-mtg-ai/
├── src/
│   ├── models/
│   │   ├── config.py       # Configuration data models
│   │   ├── email.py        # Email model with filter methods
│   │   └── meeting.py      # Meeting model with validation
│   ├── services/
│   │   ├── gmail_service.py      # Gmail API integration
│   │   ├── calendar_service.py   # Calendar API integration
│   │   └── llm_service.py        # LLM API integration
│   ├── utils/
│   │   ├── config_loader.py      # Configuration loading
│   │   ├── email_filter.py       # Email filtering logic
│   │   ├── logger.py             # Logging setup
│   │   └── storage.py            # SQLite storage
│   ├── agent.py                  # Main agent orchestration
│   └── scheduler.py              # Scheduler implementation
├── cli.py                        # CLI interface
├── send_test_emails.py           # Test email generator
├── debug_emails.py               # Debug utility
├── config.yaml                   # Configuration file
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # Documentation
```

## User Stories

### US-1: Email Filtering
**As a user**, I want to configure email filters so that only relevant emails trigger calendar event creation.

**Acceptance Criteria:**
- ✅ Configuration file supports sender, subject keywords, labels, and read status filters
- ✅ Empty filter arrays match all emails
- ✅ Agent processes only emails matching all criteria (AND logic)
- ✅ Emails not matching filters are tracked with reason "Did not match filter criteria"

### US-2: Automatic Meeting Extraction
**As a user**, I want the agent to extract meeting details from emails using AI so I don't have to manually parse email content.

**Acceptance Criteria:**
- ✅ LLM accurately extracts meeting subject, date, time, and description
- ✅ Agent handles emails with missing information gracefully
- ✅ Extraction failures are stored with reason "Could not extract valid meeting information (missing date/time)"

### US-3: Calendar Event Creation
**As a user**, I want meetings automatically added to my Google Calendar so I don't forget important appointments.

**Acceptance Criteria:**
- ✅ Calendar events are created with correct title, date, time, and description
- ✅ Events include reference to original email in description
- ✅ Duplicate events are not created for the same email
- ✅ Successfully created events are tracked with reason "Successfully created calendar event"

### US-4: Scheduled Execution
**As a user**, I want the agent to run automatically every 30 minutes so I don't have to manually trigger it.

**Acceptance Criteria:**
- ✅ Agent runs on schedule using APScheduler
- ✅ Execution logs show timestamp and results of each run
- ✅ Agent recovers gracefully from errors without stopping future runs
- ✅ Scheduler can be stopped with Ctrl+C

### US-5: Manual Execution
**As a user**, I want to manually run the agent on demand for immediate processing.

**Acceptance Criteria:**
- ✅ `python cli.py run` triggers immediate execution
- ✅ Manual runs follow same filtering and processing logic as automatic runs
- ✅ Command output shows: emails checked, filtered, meetings created, errors

### US-6: Processing Reports
**As a user**, I want to view detailed reports of all processed emails to understand what the agent is doing.

**Acceptance Criteria:**
- ✅ `python cli.py report` generates markdown report
- ✅ Report shows all checked emails (not just successful ones)
- ✅ Report includes: subject, sender, timestamp, status, and detailed reason
- ✅ Report includes summary statistics

### US-7: Quick Statistics
**As a user**, I want to quickly see how many emails have been processed and meetings created.

**Acceptance Criteria:**
- ✅ `python cli.py stats` shows total emails processed and meetings created
- ✅ Statistics are retrieved from database

### US-8: Test Email Generation
**As a user**, I want to easily generate test emails to verify the agent is working correctly.

**Acceptance Criteria:**
- ✅ `python send_test_emails.py` sends 3 test meeting emails
- ✅ Test emails contain proper meeting information (date, time, location)
- ✅ Test emails are scheduled for current week
- ✅ Test emails have subjects matching filter criteria

## CLI Commands

### Implemented Commands
1. **`python cli.py run`** - Run the agent once manually
2. **`python cli.py schedule`** - Start automatic scheduler (runs every 30 min)
3. **`python cli.py stats`** - Display quick processing statistics
4. **`python cli.py report [--output FILE]`** - Generate detailed markdown report

### Helper Scripts
1. **`python send_test_emails.py`** - Send 3 test meeting emails
2. **`python debug_emails.py`** - Debug utility to inspect fetched emails

## Security & Privacy

### Authentication
- ✅ Use OAuth 2.0 for Gmail and Calendar APIs
- ✅ Store credentials in pickle files (gmail_token.pickle, calendar_token.pickle)
- ✅ Support credential refresh automatically
- ✅ Separate OAuth tokens for different scopes

### Data Handling
- ✅ Store email metadata in SQLite database
- ✅ Store email IDs, subjects, senders, and processing status
- ✅ Keep API keys in environment variables (.env file)
- ✅ .gitignore prevents committing sensitive files

### Error Handling
- ✅ Log errors without exposing sensitive information
- ✅ Fail gracefully when API limits are reached
- ✅ Track and report authentication failures
- ✅ Continue processing on individual email failures

## Success Metrics
- **Accuracy:** ✅ Achieved - LLM extracts meeting details accurately
- **Reliability:** ✅ Achieved - Agent runs successfully on schedule
- **Performance:** ✅ Achieved - Processes emails quickly
- **User Satisfaction:** ✅ Achieved - Fully automated meeting creation

## Implementation Status

### Completed Features (v1.0)
- ✅ Gmail API integration with OAuth 2.0
- ✅ Google Calendar API integration with OAuth 2.0
- ✅ LLM integration (OpenAI and Anthropic support)
- ✅ Email filtering by sender, subject keywords, labels, read status
- ✅ Meeting information extraction using AI
- ✅ Calendar event creation with duplicate prevention
- ✅ SQLite database for tracking processed emails
- ✅ Automatic scheduling with APScheduler
- ✅ CLI interface with multiple commands
- ✅ Comprehensive reporting system
- ✅ Configuration via YAML and environment variables
- ✅ Detailed logging to file and console
- ✅ Test email generator
- ✅ Coding standards: 150 lines max per file, single responsibility, separation of concerns

### Code Quality Standards Met
- ✅ Maximum file length: 150 lines per file (strict limit)
- ✅ Single Responsibility: Each file/class/function does ONE thing
- ✅ No duplicate code: Common logic extracted into reusable functions
- ✅ Separation of Concerns: Data models, business logic, and services are separated

## Future Enhancements (Out of Scope for v1)
- Support for multiple email accounts
- Calendar conflict detection before creating events
- Email reply with confirmation of meeting creation
- Web dashboard for monitoring and configuration
- Support for recurring meetings
- Integration with other calendar platforms (Outlook, Apple Calendar)
- Custom LLM prompts via configuration
- Timezone detection and conversion
- Meeting reminder configuration
- Batch processing optimizations
- Webhook support for real-time email processing

## Deliverables

### Completed
1. ✅ Python application with all core features
2. ✅ Configuration file template with examples
3. ✅ Setup documentation (README.md, SETUP.md)
4. ✅ Authentication setup guide for Gmail and Calendar APIs
5. ✅ Installation requirements (requirements.txt)
6. ✅ User manual with CLI commands and troubleshooting
7. ✅ Test utilities (send_test_emails.py, debug_emails.py)
8. ✅ Reporting system (EMAIL_REPORT.md generation)

## Dependencies
- ✅ Gmail API access (Google Cloud project configured)
- ✅ Google Calendar API access (enabled)
- ✅ LLM API key (OpenAI or Anthropic)
- ✅ Python 3.13+ environment
- ✅ Internet connectivity for API calls

## Risks & Mitigation
| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Gmail API rate limits | High | Limit emails per run (max 50), implement backoff | ✅ Implemented |
| LLM extraction errors | Medium | Validate extracted data, log failures with reasons | ✅ Implemented |
| OAuth token expiration | Medium | Automatic token refresh implemented | ✅ Implemented |
| Email format variations | Medium | Robust LLM prompts, handle edge cases | ✅ Implemented |
| Timezone complexity | Low | Default to UTC, future enhancement | ⚠️ Future |
| API quota costs | Medium | Use cheaper models (gpt-3.5-turbo), configurable | ✅ Implemented |

## Version History
- **v1.0** (2026-02-01): Initial release with all core features implemented
