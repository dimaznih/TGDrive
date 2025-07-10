# 🚨 Quick Fix for "Peer id invalid" Error

## Your Issue
```
utils.directoryHandler - ERROR - Error fetching backup message: Peer id invalid: -1002843656111
```

## Root Cause
Your bot cannot access the Telegram storage channel `-1002843656111` because:
- The bot is not added to the channel as an administrator, OR
- The `DATABASE_BACKUP_MSG_ID=10` message doesn't exist in the channel

## ⚡ Quick Fix (2 minutes)

### Option 1: Fix Current Channel
1. **Add bot to channel**: Go to your channel → Administrators → Add your bot as admin
2. **Check message ID**: Make sure message ID 10 exists in your channel
3. **Run test**: `python3 test_bot_connection.py`
4. **Restart**: `./deploy_fix.sh`

### Option 2: Start Fresh (Recommended)
1. **Create new channel**: Create a private Telegram channel
2. **Add bot as admin**: Give it all permissions (post, edit, delete, pin)
3. **Get channel ID**: Forward a message from the channel to @userinfobot
4. **Update environment**: Change `STORAGE_CHANNEL` and set `DATABASE_BACKUP_MSG_ID=1`
5. **Clear cache**: `rm -rf cache/`
6. **Restart**: `./deploy_fix.sh`

## 🛠️ Files Created for You

- **`TELEGRAM_CHANNEL_SETUP_FIX.md`** - Complete troubleshooting guide
- **`test_bot_connection.py`** - Test your bot connection
- **`.env.example`** - Template for your environment variables
- **`deploy_fix.sh`** - Automated deployment script

## 📋 Quick Commands

```bash
# Test bot connection
python3 test_bot_connection.py

# Quick restart
./deploy_fix.sh

# Manual restart
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null
uvicorn main:app --host 0.0.0.0 --port 8000
```

## ✅ Success Indicators

When fixed, you should see:
```
utils.clients - INFO - Started - Bot Client 1
utils.directoryHandler - INFO - Drive data loaded from Telegram backup.
INFO: Uvicorn running on http://0.0.0.0:8000
```

## 🆘 If Still Not Working

1. Check **TELEGRAM_CHANNEL_SETUP_FIX.md** for detailed steps
2. Run `python3 test_bot_connection.py` and follow the error messages
3. Make sure your bot token is valid
4. Verify the channel ID is correct (should start with `-100`)

---

**Most Common Fix**: Just add your bot as an admin to the channel and restart! 🎯