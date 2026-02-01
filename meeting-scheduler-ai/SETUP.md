# Setup Guide

Complete step-by-step guide to set up the Gmail to Calendar Meeting Agent.

## Prerequisites

- Python 3.13 or higher (3.9+ also works)
- Google account with Gmail and Calendar access
- OpenAI or Anthropic API key
- Google Cloud project (free tier is sufficient)
- Internet connection

## Step-by-Step Setup

### 1. Clone and Install

Navigate to the project directory and install dependencies:

```bash
cd set-mtg-ai
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully

### 2. Google Cloud Setup

#### A. Create Project

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "Gmail Meeting Agent" (or any name you prefer)
4. Click "Create"
5. Wait for project creation to complete

#### B. Enable APIs

1. In the Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable:
   - **Gmail API**
   - **Google Calendar API**
3. Click "Enable" for each API

#### C. Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" (unless you have Google Workspace)
3. Fill in required fields:
   - **App name**: "Gmail Meeting Agent"
   - **User support email**: your email
   - **Developer contact**: your email
4. Click "Save and Continue"
5. On "Scopes" page, click "Save and Continue" (no changes needed)
6. On "Test users" page:
   - Click "Add Users"
   - Add your Gmail address
   - Click "Save"
7. Click "Save and Continue"

#### D. Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: Choose **"Desktop app"**
4. Name: "Meeting Agent Desktop"
5. Click "Create"
6. Download the JSON file (click "Download JSON")
7. Rename it to `credentials.json`
8. Place it in the project root directory (same folder as `cli.py`)

### 3. LLM API Key Setup

Choose one provider (OpenAI or Anthropic):

#### Option A: OpenAI (Recommended for beginners)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-proj-` or `sk-`)
6. **Important**: Add billing information at https://platform.openai.com/account/billing
   - Minimum $5 credit recommended for testing

#### Option B: Anthropic (Claude)

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)
6. Check that you have credits available

### 4. Configure Environment Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` file:

```bash
# For OpenAI
OPENAI_API_KEY=sk-proj-your-actual-openai-key-here

# OR for Anthropic
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
```

**Note**: Replace the placeholder with your actual API key. Keep this file secure and never commit it to Git.

### 5. Configure Email Filters

Edit `config.yaml` to customize your email filters:

```yaml
gmail:
  filters:
    senders: []  # Empty = match all, or add specific emails/domains
    subject_keywords:
      - "meeting"
      - "appointment"
      - "sync"
    labels: []  # Empty = match all, or add specific labels
    read_status: "any"  # Options: unread, read, any

calendar:
  calendar_id: "primary"
  default_duration_minutes: 60

llm:
  provider: "openai"  # or "anthropic"
  model: "gpt-3.5-turbo"  # or "claude-3-sonnet-20240229"
  api_key: "${OPENAI_API_KEY}"

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

**Tips**:
- Use `senders: []` to match all senders
- Use `labels: []` to match all labels
- Add `@domain.com` to match all emails from a domain

### 6. First Authentication

Run the agent for the first time:

```bash
python cli.py run
```

**What happens**:
1. Browser window opens for Gmail authentication
2. You'll see: "Please visit this URL to authorize this application..."
3. Log in with your Google account
4. Review permissions and click "Allow"
5. Browser window opens again for Calendar authentication
6. Log in and click "Allow" again
7. Tokens are saved as `gmail_token.pickle` and `calendar_token.pickle`

**Important**: You need to authenticate **twice** - once for Gmail, once for Calendar.

### 7. Test the Setup

#### A. Send Test Emails

```bash
python send_test_emails.py
```

**Expected output**:
```
✓ Sent: Team Meeting - Q1 Planning
✓ Sent: Sync appointment with Client ABC
✓ Sent: 1-on-1 Meeting Scheduled

✓ All test emails sent!
```

#### B. Process Emails

Wait 5 seconds, then run:

```bash
python cli.py run
```

**Expected output**:
```
=== Agent Run Complete ===
Emails checked: 3
Emails filtered: 3
Meetings created: 3
Errors: 0
```

#### C. View Results

```bash
# Quick statistics
python cli.py stats

# Detailed report
python cli.py report
```

**Expected output**:
```
=== Processing Statistics ===
Total emails processed: 3
Meetings created: 3
```

#### D. Check Google Calendar

Open [Google Calendar](https://calendar.google.com) and verify that 3 meetings were created.

## Verification Checklist

Go through this checklist to ensure everything is set up correctly:

- [ ] Python 3.9+ installed (`python --version` shows 3.9 or higher)
- [ ] Dependencies installed (`pip list` shows all required packages)
- [ ] Google Cloud project created
- [ ] Gmail API enabled in Google Cloud Console
- [ ] Google Calendar API enabled in Google Cloud Console
- [ ] OAuth consent screen configured
- [ ] Your email added as test user
- [ ] `credentials.json` file exists in project root
- [ ] `.env` file created with valid API key
- [ ] `config.yaml` configured with your preferences
- [ ] First authentication completed (tokens created)
- [ ] Test emails sent successfully
- [ ] Test run completed without errors
- [ ] Meetings visible in Google Calendar
- [ ] Report generated successfully

## Common Setup Issues

### "File not found: credentials.json"

**Problem**: OAuth credentials file is missing.

**Solution**:
1. Download OAuth credentials from Google Cloud Console
2. Make sure it's named exactly `credentials.json`
3. Place it in the project root directory (same folder as `cli.py`)

### "The OAuth client was not found"

**Problem**: Wrong credential type was created.

**Solution**:
- Make sure you created **"Desktop app"** credentials, not "Web application"
- Delete the wrong credentials and create new ones

### "Access blocked: This app's request is invalid"

**Problem**: OAuth consent screen not configured properly.

**Solution**:
1. Configure the OAuth consent screen in Google Cloud Console
2. Add your email address as a test user
3. Make sure all required fields are filled

### "Invalid API key" / "Authentication failed"

**Problem**: LLM API key is incorrect or expired.

**Solution**:
- Check that your `.env` file has the correct API key
- Verify no extra spaces or quotes around the key
- For OpenAI: Ensure billing is set up
- For Anthropic: Ensure you have available credits

### "Error code: 429 - Quota exceeded"

**Problem**: OpenAI API quota/billing issue.

**Solution**:
- Go to https://platform.openai.com/account/billing
- Add payment method
- Add at least $5 in credits

### "Scope has changed" error

**Problem**: OAuth scopes changed, old tokens are invalid.

**Solution**:
```bash
rm -f gmail_token.pickle calendar_token.pickle
python cli.py run
```
Then re-authenticate.

### Browser doesn't open for authentication

**Problem**: Server can't open browser automatically.

**Solution**:
- Look for the URL in the terminal output
- Copy the URL manually and paste into your browser
- Complete authentication there

### "No emails processed" / "Emails filtered: 0"

**Problem**: No emails match your filter criteria.

**Solution**:
1. Check filter configuration in `config.yaml`
2. Use `python debug_emails.py` to see what emails are being fetched
3. Verify emails have subjects matching your keywords
4. Try using empty filters: `senders: []`, `labels: []`

### Empty email subjects in test emails

**Problem**: Email headers not set correctly.

**Solution**: The `send_test_emails.py` script has been fixed. Make sure you have the latest version that sets headers before content.

### "Could not extract valid meeting information"

**Problem**: LLM can't find date/time in email.

**Solution**:
- Ensure emails contain clear date/time information
- Example: "Date: February 5, 2026" and "Time: 2:00 PM"
- Check logs in `./logs/agent.log` for details

## CLI Commands Reference

Once setup is complete, you can use these commands:

| Command | Description |
|---------|-------------|
| `python cli.py run` | Run agent once manually |
| `python cli.py schedule` | Start scheduler (runs every 30 min) |
| `python cli.py stats` | Display quick statistics |
| `python cli.py report` | Generate detailed markdown report |
| `python send_test_emails.py` | Send 3 test meeting emails |
| `python debug_emails.py` | Debug utility to inspect emails |

## Next Steps

### For Regular Use

1. **Manual runs**: `python cli.py run` whenever you want to process new emails
2. **Automatic mode**: `python cli.py schedule` to run every 30 minutes
3. **Monitor**: Check `python cli.py stats` periodically
4. **Reports**: Generate `python cli.py report` to review all processed emails

### For Development/Testing

1. **Clear database**: `rm -f ./data/processed_emails.db`
2. **Send test emails**: `python send_test_emails.py`
3. **Process emails**: `python cli.py run`
4. **Generate report**: `python cli.py report`
5. **Check calendar**: Verify meetings in Google Calendar

### Customization

1. **Adjust filters**: Edit `config.yaml` to match your email patterns
2. **Change LLM model**: Switch between `gpt-3.5-turbo`, `gpt-4`, or Claude models
3. **Modify schedule**: Change `schedule_interval_minutes` in config
4. **Add more keywords**: Expand `subject_keywords` list

## Security Best Practices

### File Security
- ✅ Never commit `credentials.json` to Git
- ✅ Never commit `gmail_token.pickle` or `calendar_token.pickle`
- ✅ Never commit `.env` file
- ✅ All sensitive files are in `.gitignore`

### API Key Security
- ✅ Store API keys in `.env` file only
- ✅ Use environment variables in `config.yaml`: `"${OPENAI_API_KEY}"`
- ✅ Rotate API keys periodically
- ✅ Use minimum required permissions

### OAuth Token Security
- ✅ Tokens stored locally in pickle files
- ✅ Tokens auto-refresh when expired
- ✅ Tokens are specific to your machine
- ✅ Delete tokens if compromised and re-authenticate

## Database Management

### Location
Database file: `./data/processed_emails.db`

### Clear Database (for testing)
```bash
rm -f ./data/processed_emails.db
```

### View Database (optional)
```bash
sqlite3 ./data/processed_emails.db "SELECT * FROM processed_emails;"
```

## Logging

### Log Files
- **Location**: `./logs/agent.log`
- **Level**: INFO (configurable in `config.yaml`)

### View Logs
```bash
# View recent logs
tail -f ./logs/agent.log

# View last 50 lines
tail -50 ./logs/agent.log

# Search for errors
grep ERROR ./logs/agent.log
```

## Getting Help

If you're still having issues after following this guide:

1. **Check logs**: `./logs/agent.log` has detailed error messages
2. **Review configuration**: Verify `config.yaml` and `.env` are correct
3. **Test components**:
   - `python debug_emails.py` - Check email fetching
   - `python send_test_emails.py` - Test email sending
   - `python cli.py stats` - Check database connection
4. **Verify credentials**: Make sure all API keys and OAuth tokens are valid
5. **Review README**: See [README.md](README.md) for additional troubleshooting

## Success Indicators

You'll know setup is successful when:

✅ Authentication completes without errors
✅ Test emails are sent successfully
✅ Agent processes emails and creates meetings
✅ Meetings appear in Google Calendar
✅ Reports show processed emails with details
✅ No errors in logs

## Version Information

- **Python**: 3.13+ (3.9+ compatible)
- **Setup Guide Version**: 1.0.0
- **Last Updated**: 2026-02-01
