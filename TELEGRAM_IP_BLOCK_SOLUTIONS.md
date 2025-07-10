# 🚨 Telegram IP Block Solutions - TGDrive

## Problem: IP VPS Diblokir Telegram

**Cause**: Terlalu sering restart/redeploy bot dalam waktu singkat
**Error**: "Connection timed out" / "Network issues"
**Telegram Policy**: Rate limiting untuk mencegah spam/abuse

---

## ✅ **IMMEDIATE SOLUTIONS**

### 1️⃣ **Wait & Cool Down (Simplest)**

**Tunggu 1-24 jam** sebelum restart lagi:
```bash
# Check current IP status
curl -s https://ipinfo.io/ | grep -E "(ip|country|org)"

# Wait and try later
echo "Wait 1-24 hours before restarting bot"
```

### 2️⃣ **Use Proxy/SOCKS5 (Recommended)**

Edit `utils/clients.py` untuk add proxy support:

```python
# Add proxy configuration
PROXY_CONFIG = {
    "hostname": "your_proxy_host",
    "port": 1080,
    "username": "proxy_user",  # optional
    "password": "proxy_pass"   # optional
}

# Modify client initialization
client = Client(
    name=str(client_id),
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=token,
    workdir=session_cache_path,
    proxy=PROXY_CONFIG  # Add this line
)
```

### 3️⃣ **Change VPS/IP Address**

**Option A: New VPS**
```bash
# Deploy to different IP
# Use different cloud provider (AWS, DigitalOcean, Vultr, etc.)
```

**Option B: VPS with Multiple IPs**
```bash
# Some providers allow IP rotation
# Or use floating IPs
```

---

## 🔧 **ADVANCED SOLUTIONS**

### 4️⃣ **Proxy Rotation System**

Create `config_proxy.py`:
```python
import random

PROXY_LIST = [
    {"hostname": "proxy1.com", "port": 1080},
    {"hostname": "proxy2.com", "port": 1080},
    {"hostname": "proxy3.com", "port": 1080}
]

def get_random_proxy():
    return random.choice(PROXY_LIST)
```

### 5️⃣ **Telegram Datacenter Routing**

Edit `.env` untuk specific DC:
```env
# Force specific Telegram datacenter
API_ID=123456
API_HASH=your_hash
BOT_TOKENS=your_token

# Add datacenter preference
TELEGRAM_DC=2  # Try different DCs: 1,2,3,4,5
```

### 6️⃣ **Connection Retry Logic**

Modify `utils/clients.py` with better retry:
```python
import asyncio
import random

async def start_client_with_retry(client_id, token, type, max_retries=5):
    for attempt in range(max_retries):
        try:
            # Add random delay to avoid burst connections
            await asyncio.sleep(random.uniform(5, 15))
            
            logger.info(f"Attempt {attempt+1}: Starting {type} Client {client_id}")
            
            client = Client(
                name=str(client_id),
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                bot_token=token,
                workdir=session_cache_path,
                sleep_threshold=120,  # Increase sleep threshold
                timeout=60,  # Add timeout
            )
            
            await client.start()
            logger.info(f"✅ Successfully started {type} Client {client_id}")
            return client
            
        except Exception as e:
            wait_time = (2 ** attempt) * 60  # Exponential backoff
            logger.warning(f"❌ Attempt {attempt+1} failed: {e}")
            logger.info(f"⏳ Waiting {wait_time}s before retry...")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"🚨 All attempts failed for {type} Client {client_id}")
                raise e
```

---

## 🌐 **FREE PROXY SOLUTIONS**

### Public SOCKS5 Proxies:
```bash
# Check free proxy lists
curl -s "https://api.proxyscrape.com/v2/?request=get&protocol=socks5&format=textplain" | head -10
```

### Tor as Proxy:
```bash
# Install Tor
sudo apt update && sudo apt install tor -y

# Start Tor
sudo systemctl start tor

# Use Tor proxy: 127.0.0.1:9050
```

Add to `utils/clients.py`:
```python
TOR_PROXY = {
    "hostname": "127.0.0.1",
    "port": 9050
}
```

---

## 🚀 **CLOUDFLARE TUNNEL SOLUTION**

Bypass IP restrictions using Cloudflare:

### Install Cloudflared:
```bash
# Install cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# Create tunnel
cloudflared tunnel create tgdrive

# Route through tunnel
cloudflared tunnel route ip add 0.0.0.0/0 tgdrive
```

### Route Telegram Traffic:
```yaml
# ~/.cloudflared/config.yml
tunnel: tgdrive
credentials-file: /home/ubuntu/.cloudflared/tgdrive.json

ingress:
  - hostname: api.telegram.org
    service: https://api.telegram.org
  - service: http_status:404
```

---

## ⚡ **EMERGENCY QUICK FIXES**

### Method 1: VPN + Restart
```bash
# Install and use VPN
sudo apt install openvpn -y
# Connect to VPN first, then restart bot
```

### Method 2: Mobile Hotspot
```bash
# Use mobile internet temporarily
# Change VPS networking or use different connection
```

### Method 3: Different Telegram API
```bash
# Use different API endpoints
# Some regions have different rate limits
```

---

## 🔍 **DEBUGGING IP BLOCKS**

### Check IP Status:
```bash
# Check if IP is blacklisted
curl -s "https://check-host.net/ip-info?host=$(curl -s ifconfig.me)"

# Test Telegram connectivity
curl -s "https://api.telegram.org/bot$BOT_TOKEN/getMe"
```

### Monitor Connection:
```bash
# Monitor Telegram connections
netstat -an | grep ":443"
ss -tuln | grep ":443"
```

---

## 📋 **PREVENTION STRATEGIES**

### 1. **Reduce Restart Frequency**
```bash
# Instead of frequent restarts, use:
# - Hot reload capabilities
# - Graceful shutdown/restart
# - Health checks before restart
```

### 2. **Implement Circuit Breaker**
```python
# Add to clients.py
import time

last_restart_time = 0
MIN_RESTART_INTERVAL = 300  # 5 minutes

def can_restart():
    global last_restart_time
    if time.time() - last_restart_time < MIN_RESTART_INTERVAL:
        return False
    last_restart_time = time.time()
    return True
```

### 3. **Better Error Handling**
```python
# Don't restart on every error
# Implement smart retry logic
# Use exponential backoff
```

---

## 🎯 **RECOMMENDED SOLUTION ORDER**

1. **Wait 24 hours** (simplest, free)
2. **Use free proxy/Tor** (quick fix)
3. **Implement retry logic** (permanent fix)
4. **Change VPS provider** (if needed)
5. **Use paid proxy service** (enterprise solution)

---

## 🔧 **IMPLEMENTATION COMMANDS**

### Quick Proxy Setup:
```bash
# Install Tor proxy
sudo apt update && sudo apt install tor -y
sudo systemctl start tor

# Test connection through Tor
curl --socks5 127.0.0.1:9050 https://api.telegram.org/
```

### Better Restart Script:
```bash
#!/bin/bash
# restart_safe.sh

echo "⏳ Checking if safe to restart..."
if [ -f "/tmp/last_restart" ]; then
    last=$(cat /tmp/last_restart)
    now=$(date +%s)
    diff=$((now - last))
    
    if [ $diff -lt 300 ]; then  # 5 minutes
        echo "❌ Must wait $((300 - diff)) seconds"
        exit 1
    fi
fi

echo $(($(date +%s))) > /tmp/last_restart
echo "✅ Safe to restart. Killing old process..."

sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null
sleep 5
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Problem: IP block akan resolved dalam 1-24 jam, atau gunakan proxy/VPN untuk immediate fix!**