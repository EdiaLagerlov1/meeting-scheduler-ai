#!/bin/bash

echo "🚀 Setting up Git repository for meeting-scheduler-ai"
echo ""
echo "Before running this script, make sure you've created the repository on GitHub:"
echo "https://github.com/new"
echo ""
read -p "Have you created the GitHub repository? (y/n): " created

if [ "$created" != "y" ]; then
    echo "Please create the repository first, then run this script again."
    exit 1
fi

read -p "Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "Username cannot be empty"
    exit 1
fi

echo ""
echo "Initializing Git..."
git init

echo "Adding files..."
git add .

echo "Creating commit..."
git commit -m "Initial commit: Meeting Scheduler AI

Features:
- Gmail API integration with OAuth 2.0
- Google Calendar API integration
- LLM-based meeting extraction (OpenAI & Anthropic)
- Email filtering (sender, subject, labels, read status)
- Automatic scheduling every 30 minutes
- Manual execution mode
- SQLite database for tracking
- Comprehensive reporting system
- CLI interface with multiple commands
- Test utilities and debug tools
- Complete documentation and setup guides"

echo "Adding remote..."
git remote add origin https://github.com/${username}/meeting-scheduler-ai.git

echo "Setting branch to main..."
git branch -M main

echo ""
echo "✅ Ready to push!"
echo ""
echo "Now run:"
echo "git push -u origin main"
echo ""
echo "Your repository will be at:"
echo "https://github.com/${username}/meeting-scheduler-ai"
