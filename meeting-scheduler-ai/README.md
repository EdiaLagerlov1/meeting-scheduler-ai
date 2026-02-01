# Gmail to Calendar Meeting Agent

An automated agent that monitors Gmail for emails matching predefined criteria and automatically creates Google Calendar meetings by extracting meeting details using an LLM.

## Demo

The agent automatically processes meeting emails from your Gmail inbox and creates calendar events:

**Gmail Inbox** → **AI Processing** → **Google Calendar**

![Gmail Mailbox](images/mailbox.png)
*Incoming meeting emails in Gmail*

![Google Calendar](images/calendar.png)
*Automatically created calendar events*

## Features

- **Email Monitoring**: Automatically checks Gmail for new emails
- **Smart Filtering**: Filters emails by sender, subject keywords, labels, and read status
- **AI-Powered Extraction**: Uses LLM (OpenAI or Anthropic) to extract meeting details
- **Calendar Integration**: Creates Google Calendar events with proper details
- **Duplicate Prevention**: Tracks processed emails to avoid duplicates
- **Manual & Automatic Modes**: Run on-demand or on a schedule (every 30 minutes)
- **Comprehensive Reporting**: Generate detailed reports of all processed emails
- **Configurable**: Easy YAML-based configuration with environment variables

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Gmail API
   - Google Calendar API
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth client ID"
   - Choose "Desktop app"
   - Download the credentials JSON file
   - Save it as `credentials.json` in the project root

### 3. Configure API Keys

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your LLM API key:

```
OPENAI_API_KEY=sk-your-openai-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### 4. Configure Email Filters

Edit `config.yaml` to set your email filters:

```yaml
gmail:
  filters:
    senders: []  # Empty = match all, or ["email@domain.com", "@company.com"]
    subject_keywords:
      - "meeting"
      - "appointment"
      - "sync"
    labels: []  # Empty = match all, or ["Important"]
    read_status: "any"  # Options: unread, read, any

llm:
  provider: "openai"  # Options: openai, anthropic
  model: "gpt-3.5-turbo"
  api_key: "${OPENAI_API_KEY}"
```

### 5. Run the Agent

```bash
# Run once manually
python cli.py run

# Start automatic scheduler (runs every 30 minutes)
python cli.py schedule

# View statistics
python cli.py stats

# Generate detailed report
python cli.py report
```

## CLI Commands

### Main Commands

| Command | Description |
|---------|-------------|
| `python cli.py run` | Run the agent once manually |
| `python cli.py schedule` | Start automatic scheduler (every 30 min) |
| `python cli.py stats` | Display processing statistics |
| `python cli.py report` | Generate markdown report |
| `python cli.py report --output FILE` | Generate report with custom filename |

### Testing & Development

| Script | Description |
|--------|-------------|
| `python send_test_emails.py` | Send 3 test meeting emails |
| `python debug_emails.py` | Debug utility to inspect emails |

## Project Structure

```
set-mtg-ai/
├── src/
│   ├── models/           # Data models
│   │   ├── config.py     # Configuration models
│   │   ├── email.py      # Email model with filter methods
│   │   └── meeting.py    # Meeting model with validation
│   ├── services/         # External API services
│   │   ├── gmail_service.py      # Gmail API integration
│   │   ├── calendar_service.py   # Calendar API integration
│   │   └── llm_service.py        # LLM API integration
│   ├── utils/            # Utilities
│   │   ├── config_loader.py      # Configuration loading
│   │   ├── email_filter.py       # Email filtering logic
│   │   ├── logger.py             # Logging setup
│   │   └── storage.py            # SQLite storage
│   ├── agent.py          # Main agent orchestration
│   └── scheduler.py      # Scheduling logic
├── cli.py                # Command-line interface
├── send_test_emails.py   # Test email generator
├── debug_emails.py       # Debug utility
├── config.yaml           # Configuration file
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create from .env.example)
├── README.md            # This file
├── SETUP.md             # Detailed setup guide
└── PRD.md               # Product requirements document
```

## Configuration

### config.yaml

```yaml
gmail:
  filters:
    senders: []              # List of email addresses or domains (@domain.com)
    subject_keywords: []     # Keywords to search in subject
    labels: []               # Gmail labels
    read_status: "any"       # Options: unread, read, any

calendar:
  calendar_id: "primary"     # Calendar ID or "primary"
  default_duration_minutes: 60

llm:
  provider: "openai"         # Options: openai, anthropic
  model: "gpt-3.5-turbo"     # or "claude-3-sonnet-20240229"
  api_key: "${OPENAI_API_KEY}"

agent:
  schedule_interval_minutes: 30
  max_emails_per_run: 50
  mark_as_read_after_processing: true

storage:
  database_path: "./data/processed_emails.db"

logging:
  level: "INFO"            # Options: DEBUG, INFO, WARNING, ERROR
  file_path: "./logs/agent.log"
```

### Empty Filter Arrays

Empty arrays (`[]`) in filters mean **match all**:
- `senders: []` → Match all senders
- `labels: []` → Match all labels
- `subject_keywords: []` → Match all subjects (not recommended)

## How It Works

1. **Authentication**: Authenticates with Gmail and Calendar APIs using OAuth 2.0
2. **Fetch Emails**: Retrieves recent emails from Gmail (max 50 by default)
3. **Filter**: Applies configured filters (sender, subject, labels, read status)
4. **Track**: Records all checked emails in SQLite database
5. **Extract**: Uses LLM to extract meeting details (subject, date, time, location)
6. **Validate**: Validates extracted meeting information
7. **Create Event**: Creates calendar event with extracted information
8. **Mark Processed**: Stores email ID to prevent duplicates

## Email Processing Report

Generate detailed reports showing all processed emails:

```bash
python cli.py report
```

Report includes:
- **Summary**: Total emails, meetings created, failures
- **Detailed Table**: Subject, Sender, Timestamp, Status, Reason
- **Reasons**:
  - ✅ "Successfully created calendar event"
  - ❌ "Did not match filter criteria (subject keywords)"
  - ❌ "Could not extract valid meeting information (missing date/time)"

### Actual Report Results

**Generated**: 2026-02-01 02:21:49
**Total Emails Processed**: 4

**Summary**:
- ✅ Meetings Created: 3
- ❌ Meetings Failed: 1

**Processed Emails**:

| # | Subject | Sender | Processed At | Meeting Created | Reason |
|---|---------|--------|--------------|-----------------|--------|
| 1 | Team Meeting - Q1 Planning | elagerlov@gmail.com | 2026-02-01 00:21 | ✅ Yes | Successfully created calendar event |
| 2 | Sync appointment with Client ABC | elagerlov@gmail.com | 2026-02-01 00:21 | ✅ Yes | Successfully created calendar event |
| 3 | 1-on-1 Meeting Scheduled | elagerlov@gmail.com | 2026-02-01 00:21 | ✅ Yes | Successfully created calendar event |
| 4 | test | Edia Lagerlov <edialagerlov... | 2026-02-01 00:21 | ❌ No | Did not match filter criteria (subject keywords) |

## Testing

### Send Test Emails

```bash
python send_test_emails.py
```

This sends 3 test emails with:
- Team Meeting - Q1 Planning (tomorrow, 2:00 PM)
- Sync appointment with Client ABC (in 2 days, 10:30 AM)
- 1-on-1 Meeting Scheduled (in 3 days, 3:30 PM)

### Process Test Emails

```bash
python cli.py run
```

### View Results

```bash
# Quick stats
python cli.py stats

# Detailed report
python cli.py report

# Check your Google Calendar
```

## First Run

On the first run, you'll be prompted to authorize the application:

1. A browser window will open
2. Log in with your Google account
3. Grant the requested permissions
4. Tokens will be saved for future use

**Note**: You'll need to authenticate twice:
- Once for Gmail access
- Once for Calendar access

## Troubleshooting

### "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Place the file in the project root directory

### "No module named 'src'"
- Run commands from the project root directory
- Ensure you're using Python 3.9+

### "Invalid API key" / "Quota exceeded"
- Check that your `.env` file has the correct API key
- For OpenAI: Add billing at https://platform.openai.com/account/billing
- For Anthropic: Check credits at https://console.anthropic.com/

### "No emails processed"
- Check your filter configuration in `config.yaml`
- Verify you have emails matching the criteria
- Check logs in `./logs/agent.log`
- Use `python debug_emails.py` to see what emails are being fetched

### Empty subjects in emails
- Make sure `send_test_emails.py` sets headers before content
- Headers should use capitalized keys: `'Subject'`, `'To'`

### LLM extraction failures
- Ensure emails contain clear date/time information
- Check that the LLM model is available for your API key
- Review logs for specific error messages

## Example Email Content

For successful meeting extraction, emails should contain:

```
Subject: Team Meeting - Project Update

Hi Team,

Let's schedule a meeting to discuss the project update.

Date: February 5, 2026
Time: 2:00 PM
Duration: 1 hour
Location: Conference Room A

Agenda:
- Review progress
- Discuss blockers
- Plan next steps

Thanks!
```

## Database

The agent uses SQLite to track processed emails:

**Database file**: `./data/processed_emails.db`

**Schema**:
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

**Clear database** (for testing):
```bash
rm -f ./data/processed_emails.db
```

## Logging

Logs are written to both console and file:
- **File**: `./logs/agent.log`
- **Level**: Configurable in `config.yaml` (DEBUG, INFO, WARNING, ERROR)

View logs:
```bash
tail -f ./logs/agent.log
```

## Security

### Credentials
- OAuth tokens stored in: `gmail_token.pickle`, `calendar_token.pickle`
- API keys stored in: `.env` file
- All sensitive files are in `.gitignore`

### Best Practices
- Never commit `credentials.json`, token files, or `.env`
- Use environment variables for API keys
- Tokens auto-refresh when expired
- Keep your Google Cloud project credentials secure

## Development

### Code Standards
- **Maximum file length**: 150 lines per file (strict limit)
- **Single Responsibility**: Each file/class/function does ONE thing
- **No duplicate code**: Common logic extracted into reusable functions
- **Separation of Concerns**: Data models, business logic, and services are separated

### Running Tests

```bash
# Clear database
rm -f ./data/processed_emails.db

# Send test emails
python send_test_emails.py

# Wait a few seconds for emails to arrive
sleep 5

# Process emails
python cli.py run

# Generate report
python cli.py report
```

## Technology Stack

- **Python**: 3.13+
- **Gmail API**: google-api-python-client 2.111.0
- **Calendar API**: google-api-python-client 2.111.0
- **LLM**: openai 2.16.0, anthropic 0.77.0
- **Scheduler**: APScheduler 3.10.4
- **CLI**: click 8.1.7
- **Config**: PyYAML 6.0.1, python-dotenv 1.0.0
- **Database**: SQLite3 (built-in)
- **Logging**: Python logging (built-in)

## Supported LLM Providers

### OpenAI
- Models: `gpt-4`, `gpt-3.5-turbo` (recommended for cost)
- Get API key: https://platform.openai.com/api-keys

### Anthropic (Claude)
- Models: `claude-3-sonnet-20240229`
- Get API key: https://console.anthropic.com/

## FAQ

**Q: How often does the agent run in automatic mode?**
A: Every 30 minutes (configurable in `config.yaml`)

**Q: Can I run it manually?**
A: Yes, use `python cli.py run`

**Q: Will it create duplicate meetings?**
A: No, processed emails are tracked in the database

**Q: Can I filter by multiple criteria?**
A: Yes, all filters use AND logic (must match all criteria)

**Q: What happens if meeting extraction fails?**
A: The email is marked as processed with a failure reason, no calendar event is created

**Q: Can I see which emails were checked but not processed?**
A: Yes, run `python cli.py report` to see all emails with reasons

**Q: How do I stop the scheduler?**
A: Press `Ctrl+C`

**Q: Can I use multiple email accounts?**
A: Not in v1.0, this is a future enhancement

## Support & Documentation

- **Setup Guide**: See [SETUP.md](SETUP.md) for detailed setup instructions
- **PRD**: See [PRD.md](PRD.md) for complete product requirements
- **Logs**: Check `./logs/agent.log` for detailed error messages
- **Issues**: Review configuration and check logs

## Version

**Current Version**: 1.0.0
**Release Date**: 2026-02-01

## License

MIT License

## Contributing

This is a personal project. Feel free to fork and modify for your own use.

## Changelog

### v1.0.0 (2026-02-01)
- Initial release
- Gmail API integration with OAuth 2.0
- Google Calendar API integration
- LLM-based meeting extraction (OpenAI & Anthropic)
- Email filtering (sender, subject, labels, read status)
- Automatic scheduling (every 30 minutes)
- Manual execution mode
- SQLite database for tracking
- Comprehensive reporting system
- CLI interface with multiple commands
- Test utilities and debug tools
