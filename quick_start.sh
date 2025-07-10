#!/bin/bash

# TGDrive Quick Start Script - Separated Deployment System
# This script sets up and starts the new separated bot and web services

echo "🚀 TGDrive Separated Deployment - Quick Start"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed!"
    exit 1
fi

print_step "1. Checking current configuration..."

# Check if .env exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    echo "Please create .env file with your bot configuration."
    exit 1
fi

# Show current bot token (partially hidden)
if [ -f ".env" ]; then
    BOT_TOKEN=$(grep "^BOT_TOKENS=" .env | cut -d'=' -f2)
    if [ ! -z "$BOT_TOKEN" ]; then
        PARTIAL_TOKEN="${BOT_TOKEN:0:12}...${BOT_TOKEN: -6}"
        print_status "Found bot token: $PARTIAL_TOKEN"
    else
        print_error "No bot token found in .env!"
        exit 1
    fi
fi

print_step "2. Stopping any existing services..."

# Stop any existing processes
python3 manage.py stop-all 2>/dev/null
pkill -f "bot_service.py" 2>/dev/null
pkill -f "uvicorn main:app" 2>/dev/null

print_status "Existing services stopped"

print_step "3. Cleaning up old cache and session files..."

# Clean up old files
rm -rf cache/
rm -rf shared/
rm -rf pids/
mkdir -p cache shared pids

print_status "Cache and session files cleaned"

print_step "4. Testing bot token (checking for flood wait)..."

# Test bot token
python3 check_flood_wait.py

if [ $? -ne 0 ]; then
    print_warning "Bot token test failed or flood wait detected"
    echo "You can:"
    echo "  1. Wait for flood wait to expire"
    echo "  2. Create new bot token: python3 update_bot_token.py <NEW_TOKEN>"
    echo "  3. Continue anyway (may fail)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

print_step "5. Starting TGDrive services..."

# Start services
print_status "Starting bot service..."
python3 manage.py start-bot

sleep 5

print_status "Starting web service..."
python3 manage.py start-web

sleep 3

print_step "6. Checking service status..."

# Check status
python3 manage.py status

print_step "7. Testing web interface..."

# Test web interface
sleep 5
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 2>/dev/null)

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "405" ]; then
    print_status "✅ Web interface is accessible!"
    echo
    echo "🎉 TGDrive is now running!"
    echo
    echo "📍 Access your TGDrive at:"
    echo "   Local:    http://localhost:8000"
    echo "   Network:  http://$(hostname -I | awk '{print $1}'):8000"
    echo
    echo "🔧 Management commands:"
    echo "   Status:      python3 manage.py status"
    echo "   Restart web: python3 manage.py restart-web"
    echo "   Restart bot: python3 manage.py restart-bot"
    echo "   Stop all:    python3 manage.py stop-all"
    echo
    echo "📚 Read SEPARATED_DEPLOY_GUIDE.md for complete documentation"
    echo
else
    print_error "Web interface is not accessible (HTTP: $HTTP_STATUS)"
    echo
    echo "🔍 Troubleshooting:"
    echo "   Check status: python3 manage.py status"
    echo "   Check logs:   python3 web_service.py"
    echo "   Manual start: python3 manage.py start-web --port 8080"
fi

print_step "8. Service management summary:"
echo
echo "  🤖 Bot Service (Independent):"
echo "     - Handles Telegram operations"
echo "     - Runs continuously, no restart needed for web changes"
echo "     - Avoids flood wait issues"
echo
echo "  🌐 Web Service (Independent):"
echo "     - Handles web interface"
echo "     - Can restart anytime without affecting bot"
echo "     - Safe for development and updates"
echo
echo "✅ Setup complete! Your TGDrive is now running with separated services."