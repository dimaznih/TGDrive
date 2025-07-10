#!/bin/bash

# TGDrive Deployment Fix Script
echo "🔧 TGDrive Deployment Fix Script"
echo "================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to kill existing processes
kill_existing() {
    echo "🛑 Stopping existing TGDrive processes..."
    
    # Method 1: Kill by port
    if sudo lsof -t -i:8000 >/dev/null 2>&1; then
        echo "   Killing processes on port 8000..."
        sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null
        sleep 2
    fi
    
    # Method 2: Kill by process name
    if pgrep -f "uvicorn main:app" >/dev/null 2>&1; then
        echo "   Killing uvicorn processes..."
        sudo pkill -9 -f "uvicorn main:app" 2>/dev/null
        sleep 2
    fi
    
    # Method 3: Kill by python processes running main.py
    if pgrep -f "python.*main" >/dev/null 2>&1; then
        echo "   Killing python main processes..."
        sudo pkill -9 -f "python.*main" 2>/dev/null
        sleep 2
    fi
    
    echo "✅ Existing processes stopped"
}

# Function to check dependencies
check_dependencies() {
    echo "📋 Checking dependencies..."
    
    if ! command_exists python3; then
        echo "❌ Python3 not found. Installing..."
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
    
    if ! command_exists pip3; then
        echo "❌ pip3 not found. Installing..."
        sudo apt-get install -y python3-pip
    fi
    
    # Check if uvicorn is installed
    if ! python3 -c "import uvicorn" 2>/dev/null; then
        echo "❌ uvicorn not found. Installing requirements..."
        pip3 install -r requirements.txt
    fi
    
    echo "✅ Dependencies checked"
}

# Function to test bot connection
test_connection() {
    echo "🔍 Testing bot connection..."
    if [ -f "test_bot_connection.py" ]; then
        echo "   Running connection test..."
        python3 test_bot_connection.py
        echo ""
        read -p "❓ Did the connection test pass? (y/N): " test_passed
        if [[ $test_passed =~ ^[Yy]$ ]]; then
            echo "✅ Connection test passed!"
            return 0
        else
            echo "❌ Connection test failed. Please fix the issues first."
            echo "📖 Check TELEGRAM_CHANNEL_SETUP_FIX.md for help"
            return 1
        fi
    else
        echo "⚠️  test_bot_connection.py not found, skipping test"
        return 0
    fi
}

# Function to backup data
backup_data() {
    echo "💾 Creating backup..."
    
    if [ -d "cache" ]; then
        cp -r cache cache_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null
        echo "✅ Cache backup created"
    fi
    
    # Backup .env if it exists
    if [ -f ".env" ]; then
        cp .env .env.backup_$(date +%Y%m%d_%H%M%S)
        echo "✅ Environment backup created"
    fi
}

# Function to clear cache if needed
clear_cache() {
    read -p "❓ Clear cache directory? This will reset your drive data. (y/N): " clear_cache
    if [[ $clear_cache =~ ^[Yy]$ ]]; then
        echo "🗑️  Clearing cache..."
        rm -rf cache/
        mkdir -p cache/
        echo "✅ Cache cleared"
    else
        echo "⏭️  Cache preserved"
    fi
}

# Function to start application
start_app() {
    echo "🚀 Starting TGDrive..."
    
    # Make sure we're in the right directory
    if [ ! -f "main.py" ]; then
        echo "❌ main.py not found. Make sure you're in the TGDrive directory."
        exit 1
    fi
    
    # Start the application
    echo "   Starting uvicorn server on port 8000..."
    echo "   Press Ctrl+C to stop the server"
    echo "   Access your TGDrive at: http://your-server-ip:8000"
    echo ""
    
    # Run with nohup to keep it running in background (optional)
    read -p "❓ Run in background? (y/N): " run_background
    if [[ $run_background =~ ^[Yy]$ ]]; then
        nohup uvicorn main:app --host 0.0.0.0 --port 8000 > tgdrive.log 2>&1 &
        echo "✅ TGDrive started in background"
        echo "📝 Check logs with: tail -f tgdrive.log"
        echo "🛑 Stop with: sudo kill -9 $(sudo lsof -t -i:8000)"
    else
        uvicorn main:app --host 0.0.0.0 --port 8000
    fi
}

# Main script
main() {
    echo "🎯 Starting deployment fix process..."
    echo ""
    
    # Step 1: Kill existing processes
    kill_existing
    echo ""
    
    # Step 2: Check dependencies
    check_dependencies
    echo ""
    
    # Step 3: Backup data
    backup_data
    echo ""
    
    # Step 4: Test connection (optional)
    read -p "❓ Test bot connection before starting? (Y/n): " test_conn
    if [[ ! $test_conn =~ ^[Nn]$ ]]; then
        if ! test_connection; then
            echo "❌ Aborting deployment due to connection issues"
            exit 1
        fi
        echo ""
    fi
    
    # Step 5: Clear cache (optional)
    clear_cache
    echo ""
    
    # Step 6: Start application
    start_app
}

# Script options
case "${1:-}" in
    "kill")
        kill_existing
        ;;
    "test")
        test_connection
        ;;
    "clear")
        clear_cache
        ;;
    "start")
        start_app
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  kill     Kill existing TGDrive processes"
        echo "  test     Test bot connection only"
        echo "  clear    Clear cache directory"
        echo "  start    Start TGDrive server"
        echo "  help     Show this help message"
        echo ""
        echo "No option: Run full deployment process"
        ;;
    *)
        main
        ;;
esac