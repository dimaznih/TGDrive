#!/bin/bash
# 🛡️ Safe Restart Script - Prevent Telegram IP Block
# Usage: ./restart_safe.sh

echo "🔍 Checking if safe to restart TGDrive..."

# Check if restart cooldown is active
if [ -f "/tmp/last_restart" ]; then
    last=$(cat /tmp/last_restart)
    now=$(date +%s)
    diff=$((now - last))
    
    # 5 minute cooldown period
    if [ $diff -lt 300 ]; then
        remaining=$((300 - diff))
        echo "❌ COOLDOWN ACTIVE: Must wait ${remaining} seconds before restart"
        echo "   Last restart: $(date -d @$last)"
        echo "   Next allowed: $(date -d @$((last + 300)))"
        exit 1
    fi
fi

# Record this restart time
echo $(($(date +%s))) > /tmp/last_restart
echo "✅ Safe to restart. Proceeding..."

# Check if Tor is running
if ! curl --socks5 127.0.0.1:9050 -s --max-time 5 https://api.telegram.org/ > /dev/null 2>&1; then
    echo "⚠️  Tor proxy not responding. Starting Tor..."
    pkill tor 2>/dev/null
    tor --quiet &
    sleep 5
    
    if curl --socks5 127.0.0.1:9050 -s --max-time 5 https://api.telegram.org/ > /dev/null 2>&1; then
        echo "✅ Tor proxy started successfully"
    else
        echo "❌ Tor proxy failed to start"
        exit 1
    fi
else
    echo "✅ Tor proxy is working"
fi

# Kill existing TGDrive process
echo "🔄 Stopping existing TGDrive process..."
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null && echo "✅ Old process killed"

# Wait a bit
echo "⏳ Waiting 3 seconds..."
sleep 3

# Check .env configuration
if [ ! -f ".env" ]; then
    echo "❌ ERROR: .env file not found!"
    echo "   Run: cp sample.env .env && nano .env"
    exit 1
fi

# Start TGDrive with proxy
echo "🚀 Starting TGDrive with Tor proxy..."
uvicorn main:app --host 0.0.0.0 --port 8000

echo "✅ TGDrive restarted safely via Tor proxy!"