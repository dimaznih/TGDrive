# TGDrive Storage Channel Setup Fix

## Problem
You're getting this error: `Error fetching backup message: Peer id invalid: -1002843656111`

This means your bot cannot access the Telegram storage channel. Here's how to fix it:

## Solution Steps

### 1. Create/Setup the Storage Channel

#### Option A: Create a New Channel
1. Open Telegram and create a new **channel** (not group)
2. Make it **private** (recommended for security)
3. Give it a name like "TGDrive Storage"
4. Copy the channel link

#### Option B: Use Existing Channel
1. Make sure you're the owner/admin of the channel
2. Get the channel link

### 2. Add Your Bot to the Channel

1. Open your storage channel
2. Click on channel name → **Administrators**
3. Click **Add Administrator**
4. Search for your bot username (the one you created with @BotFather)
5. Add the bot and give it these permissions:
   - ✅ **Post Messages**
   - ✅ **Edit Messages** 
   - ✅ **Delete Messages**
   - ✅ **Pin Messages**
   - ✅ **Add Subscribers** (optional)

### 3. Get the Correct Channel ID

#### Method 1: Using @userinfobot
1. Forward any message from your channel to @userinfobot
2. It will show you the channel ID (should look like `-1001234567890`)

#### Method 2: Using Web Telegram
1. Open https://web.telegram.org
2. Go to your channel
3. Look at the URL: `https://web.telegram.org/z/#-1001234567890`
4. The number after `#` is your channel ID

#### Method 3: Using your bot
1. Add this to your channel temporarily
2. Check logs for the channel ID

### 4. Create the Initial Backup Message

The application expects a specific backup message in your channel. Here's how to create it:

#### Option A: Manual Creation
1. Go to your storage channel
2. Send a text message: "TGDrive Initial Setup - Database will be created automatically"
3. Note the message ID (usually starts from 1, 2, 3...)

#### Option B: Let the app create it
The app should create it automatically, but if it fails, use Option A.

### 5. Update Your Environment Variables

Update your `.env` file or environment variables:

```env
# Your updated values
API_ID=24783879
API_HASH=935a8934034dfd64ecce5e9854fa071b
BOT_TOKENS=7914171749:AAHPJkVrKZKcvMLmg7A5UxtPpjUSOY2ezeI
STORAGE_CHANNEL=-1002843656111  # ← Make sure this is correct
DATABASE_BACKUP_MSG_ID=1  # ← Usually 1 for the first message
DATABASE_BACKUP_TIME=60
WEBSITE_URL=http://209.74.81.235:8000
MAIN_BOT_TOKEN=7914171749:AAHPJkVrKZKcvMLmg7A5UxtPpjUSOY2ezeI
ADMIN_PASSWORD=123
TELEGRAM_ADMIN_IDS=7691463286,5381870056,5092392994,1841535556,1446366033,6137698413,5366835263
```

### 6. Test Bot Access

Create a simple test script to verify your bot can access the channel:

```python
import asyncio
from pyrogram import Client

async def test_channel_access():
    API_ID = 24783879
    API_HASH = "935a8934034dfd64ecce5e9854fa071b"
    BOT_TOKEN = "7914171749:AAHPJkVrKZKcvMLmg7A5UxtPpjUSOY2ezeI"
    STORAGE_CHANNEL = -1002843656111
    
    client = Client("test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    
    try:
        await client.start()
        
        # Test 1: Send a message
        msg = await client.send_message(STORAGE_CHANNEL, "Test message - bot can access channel!")
        print(f"✅ Bot can send messages. Message ID: {msg.id}")
        
        # Test 2: Get channel info
        chat = await client.get_chat(STORAGE_CHANNEL)
        print(f"✅ Channel info: {chat.title}")
        
        # Test 3: Get messages
        async for message in client.get_chat_history(STORAGE_CHANNEL, limit=5):
            print(f"Message {message.id}: {message.text[:50] if message.text else 'Media'}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.stop()

if __name__ == "__main__":
    asyncio.run(test_channel_access())
```

### 7. Common Issues and Solutions

#### Issue: "Peer id invalid"
- **Solution**: Channel ID is wrong or bot not added to channel
- **Check**: Verify channel ID and bot permissions

#### Issue: "Chat not found" 
- **Solution**: Channel doesn't exist or is deleted
- **Check**: Make sure channel exists and is accessible

#### Issue: "Bot was blocked by the user"
- **Solution**: Unblock the bot in the channel
- **Check**: Remove and re-add bot to channel

#### Issue: "Message not found"
- **Solution**: DATABASE_BACKUP_MSG_ID is wrong
- **Check**: Use message ID 1 or create a new message

### 8. Alternative: Reset Everything

If nothing works, here's how to start fresh:

1. **Create a new channel**
2. **Add your bot as admin** 
3. **Get the new channel ID**
4. **Update STORAGE_CHANNEL in your env**
5. **Set DATABASE_BACKUP_MSG_ID=1**
6. **Delete the cache folder**: `rm -rf cache/`
7. **Restart the application**

### 9. Restart Your Application

After making changes:

```bash
# Kill existing process
sudo pkill -f "uvicorn main:app"

# Or if using specific port
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null

# Start fresh
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 10. Security Recommendations

1. **Use a private channel** for storage
2. **Don't share your storage channel** with others
3. **Regularly backup your drive.data file**
4. **Use strong admin passwords**
5. **Limit admin access** to trusted users only

---

## Quick Fix Summary

The most likely fix for your specific case:

1. **Verify your bot is admin** in channel `-1002843656111`
2. **Send a test message** to the channel manually
3. **Set DATABASE_BACKUP_MSG_ID=1** (or the message ID you created)
4. **Restart the application**

If that doesn't work, create a new channel and update your `STORAGE_CHANNEL` environment variable.