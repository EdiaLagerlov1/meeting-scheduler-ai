# GitHub Repository Setup Guide

## Repository Name: meeting-scheduler-ai

Follow these steps to create and push this project to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `meeting-scheduler-ai`
3. Description: `Automated agent that monitors Gmail and creates Google Calendar meetings using AI`
4. Visibility: Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Initialize Git (if not already done)

```bash
# Navigate to project directory
cd /Users/edialagerlov/25D_NEW/L34/set-mtg-ai

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Gmail to Calendar Meeting Scheduler AI

- Gmail API integration with OAuth 2.0
- Google Calendar API integration
- LLM-based meeting extraction (OpenAI & Anthropic)
- Email filtering (sender, subject, labels, read status)
- Automatic scheduling (every 30 minutes)
- Manual execution mode
- SQLite database for tracking
- Comprehensive reporting system
- CLI interface with multiple commands
- Test utilities and debug tools"
```

## Step 3: Add Remote and Push

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/meeting-scheduler-ai.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 4: Verify on GitHub

1. Go to `https://github.com/YOUR_GITHUB_USERNAME/meeting-scheduler-ai`
2. Verify all files are present
3. Check that README displays correctly
4. Verify images are visible

## Step 5: Add Repository Description and Topics

On your GitHub repository page:

1. Click "About" ⚙️ (gear icon)
2. Add description: `Automated agent that monitors Gmail and creates Google Calendar meetings using AI`
3. Add topics:
   - `gmail-api`
   - `google-calendar`
   - `openai`
   - `anthropic`
   - `python`
   - `automation`
   - `ai`
   - `llm`
   - `meeting-scheduler`
   - `email-automation`

## Files Already Configured

✅ `.gitignore` - Prevents committing sensitive files
✅ `README.md` - Main documentation with screenshots
✅ `SETUP.md` - Detailed setup instructions
✅ `PRD.md` - Product requirements
✅ `requirements.txt` - Python dependencies
✅ `LICENSE` - MIT License (if you want to add one)

## Sensitive Files (Already in .gitignore)

These files will NOT be committed:

- `credentials.json` - OAuth credentials
- `gmail_token.pickle` - Gmail auth token
- `calendar_token.pickle` - Calendar auth token
- `send_email_token.pickle` - Email send token
- `.env` - Environment variables with API keys
- `*.db` - Database files
- `*.log` - Log files

## Optional: Add License

If you want to add an MIT license:

```bash
# Create LICENSE file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Add and commit
git add LICENSE
git commit -m "Add MIT License"
git push
```

## Repository Badges (Optional)

Add these to the top of your README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

## Quick Commands Summary

```bash
# 1. Initialize and commit
git init
git add .
git commit -m "Initial commit: Gmail to Calendar Meeting Scheduler AI"

# 2. Add remote (replace YOUR_GITHUB_USERNAME)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/meeting-scheduler-ai.git

# 3. Push to GitHub
git branch -M main
git push -u origin main
```

## Future Updates

When you make changes:

```bash
# Check status
git status

# Add changed files
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Troubleshooting

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/meeting-scheduler-ai.git
```

### Authentication Issues
GitHub requires personal access token for HTTPS:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

Or use SSH:
```bash
git remote set-url origin git@github.com:YOUR_GITHUB_USERNAME/meeting-scheduler-ai.git
```

## Repository URL

Once created, your repository will be at:
**https://github.com/YOUR_GITHUB_USERNAME/meeting-scheduler-ai**

## Clone Command (for others)

Others can clone your repository with:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/meeting-scheduler-ai.git
cd meeting-scheduler-ai
```
