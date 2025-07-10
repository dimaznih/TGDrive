# 🔧 TGDrive Telegram Setup Guide

## Error Yang Terjadi
```
Unable to connect due to network issues: Connection timed out
```

**Root Cause**: Missing Telegram API credentials in `.env` file

## ✅ **SOLUTION: Setup Telegram Credentials**

### Step 1: Buat Telegram API Credentials

1. **Get API_ID & API_HASH**:
   - Visit: https://my.telegram.org/auth
   - Login dengan nomor Telegram
   - Go to "API Development"
   - Create new application
   - Copy `API_ID` dan `API_HASH`

2. **Create Telegram Bot**:
   - Chat dengan @BotFather di Telegram  
   - Send `/newbot`
   - Ikuti instruksi untuk nama bot
   - Copy **Bot Token** yang diberikan

3. **Create Storage Channel**:
   - Buat channel Telegram private
   - Add bot sebagai admin dengan full permissions
   - Forward message dari channel ke @userinfobot
   - Copy **Channel ID** (format: -100xxxxxxxxx)

4. **Get Database Backup Message ID**:
   - Send message apa saja ke storage channel
   - Forward message tersebut ke @userinfobot  
   - Copy **Message ID**

### Step 2: Create .env File

```bash
# Copy dari sample.env dan edit
cp sample.env .env
```

Edit `.env` dengan credentials yang benar:

```env
# Required Vars
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKENS=123456789:your_bot_token_here
STORAGE_CHANNEL=-1001234567890
DATABASE_BACKUP_MSG_ID=123

# Optional Vars  
ADMIN_PASSWORD=your_admin_password
SLEEP_THRESHOLD=60
DATABASE_BACKUP_TIME=60
```

### Step 3: Restart Server

```bash
# Kill existing server
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null

# Start with new config
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🎯 **QUICK FIX Commands**

```bash
# 1. Copy sample to actual config
cp sample.env .env

# 2. Edit with your credentials
nano .env

# 3. Restart server
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null && uvicorn main:app --host 0.0.0.0 --port 8000
```

## ⚡ **Expected Success Output**

Setelah config benar, output harus seperti ini:
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
utils.extra - INFO - Cache and downloads directory reset
utils.clients - INFO - Initializing Clients
utils.clients - INFO - Starting - Bot Client 1
utils.clients - INFO - Started - Bot Client 1
utils.clients - INFO - Clients Initialized
INFO:     Application startup complete.
```

## 🔍 **Troubleshooting**

1. **Invalid token**: Double check bot token dari @BotFather
2. **Invalid API credentials**: Re-create di my.telegram.org
3. **Wrong channel ID**: Pastikan format -100xxxxxxxxx
4. **Bot not admin**: Add bot ke channel sebagai admin
5. **Network issues**: Check firewall/VPS network settings

## 📝 **Notes**

- BOT_TOKENS dapat multiple (comma separated) untuk load balancing
- STRING_SESSIONS untuk premium features (optional)
- STORAGE_CHANNEL harus private channel  
- Bot harus punya admin permissions di channel