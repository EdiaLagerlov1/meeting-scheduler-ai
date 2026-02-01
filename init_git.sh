#!/bin/bash

# Initialize Git Repository for meeting-scheduler-ai
# Run this script after creating the repository on GitHub

echo "🚀 Initializing Git Repository for meeting-scheduler-ai"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if already initialized
if [ -d ".git" ]; then
    echo "⚠️  Git repository already initialized"
    read -p "Do you want to continue? This will NOT delete your existing .git (y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "Aborted."
        exit 0
    fi
else
    # Initialize git repository
    echo "📦 Initializing Git repository..."
    git init
fi

# Prompt for GitHub username
echo ""
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub username cannot be empty"
    exit 1
fi

# Add all files
echo ""
echo "📝 Adding files to Git..."
git add .

# Create initial commit
echo ""
echo "💾 Creating initial commit..."
git commit -m "Initial commit: Meeting Scheduler AI

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

# Add remote
echo ""
echo "🔗 Adding remote repository..."
git remote add origin "https://github.com/${github_username}/meeting-scheduler-ai.git"

# Rename branch to main
echo ""
echo "🌿 Setting branch to main..."
git branch -M main

# Show status
echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Create repository on GitHub:"
echo "   https://github.com/new"
echo "   Repository name: meeting-scheduler-ai"
echo "   DO NOT initialize with README, .gitignore, or license"
echo ""
echo "2. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Your repository will be at:"
echo "   https://github.com/${github_username}/meeting-scheduler-ai"
echo ""
echo "📖 See GITHUB_SETUP.md for detailed instructions"
