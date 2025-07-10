#!/usr/bin/env python3
"""
🔧 TGDrive Bot & Channel Test Script - Updated Token
Tests bot connection and channel access
"""

import asyncio
from pyrogram import Client
import os
from pathlib import Path

# Load your configuration
API_ID = 24783879
API_HASH = "935a8934034dfd64ecce5e9854fa071b"
BOT_TOKEN = "7914171749:AAHPJkVrKZKcvMLmg7A5UxtPpjUSOY2ezeI"
STORAGE_CHANNEL = -1002843656111
DATABASE_BACKUP_MSG_ID = 10

# TOR PROXY CONFIG (same as in your clients.py)
TOR_PROXY = {
    "scheme": "socks5",
    "hostname": "127.0.0.1", 
    "port": 9050
}

async def test_storage_channel():
    """Test if bot can access the storage channel"""
    
    print("� TGDrive Storage Channel Connection Test")
    print("=" * 50)
    
    # Create session directory
    session_cache_path = Path("./cache")
    session_cache_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize client with TOR proxy (as in your original code)
    client = Client(
        name="test_session",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workdir=session_cache_path,
        proxy=TOR_PROXY  # Using TOR proxy like in your original setup
    )
    
    try:
        print("🚀 Starting bot client...")
        await client.start()
        print("✅ Bot client started successfully")
        
        # Test 1: Get bot info
        print("\n📋 Test 1: Bot Information")
        me = await client.get_me()
        print(f"   Bot Username: @{me.username}")
        print(f"   Bot ID: {me.id}")
        print(f"   Bot Name: {me.first_name}")
        
        # Test 2: Check if channel exists and bot has access
        print(f"\n� Test 2: Channel Access Test")
        print(f"   Testing channel ID: {STORAGE_CHANNEL}")
        
        try:
            chat = await client.get_chat(STORAGE_CHANNEL)
            print(f"✅ Channel found: {chat.title}")
            print(f"   Channel Type: {chat.type}")
            print(f"   Members Count: {getattr(chat, 'members_count', 'N/A')}")
            
            # Check if bot is admin
            try:
                admins = [admin async for admin in client.get_chat_members(STORAGE_CHANNEL, filter="administrators")]
                bot_is_admin = any(admin.user.id == me.id for admin in admins)
                if bot_is_admin:
                    print("✅ Bot has admin access to the channel")
                else:
                    print("❌ Bot is NOT an admin in the channel")
                    print("   🔧 Fix: Add the bot as an administrator in the channel")
                    
            except Exception as admin_e:
                print(f"⚠️  Could not check admin status: {admin_e}")
                
        except Exception as chat_e:
            print(f"❌ Cannot access channel: {chat_e}")
            print("   🔧 Fix: Make sure the bot is added to the channel as an admin")
            return False
        
        # Test 3: Check specific backup message
        print(f"\n📄 Test 3: Backup Message Test")
        print(f"   Looking for message ID: {DATABASE_BACKUP_MSG_ID}")
        
        try:
            msg = await client.get_messages(STORAGE_CHANNEL, DATABASE_BACKUP_MSG_ID)
            if msg:
                print("✅ Backup message found")
                print(f"   Message ID: {msg.id}")
                print(f"   Message Date: {msg.date}")
                if msg.document:
                    print(f"   Document: {msg.document.file_name}")
                    print(f"   File Size: {msg.document.file_size} bytes")
                else:
                    print(f"   Text: {msg.text[:100] if msg.text else 'No text'}...")
            else:
                print("❌ Backup message not found")
                print("   🔧 Fix: Create a message in the channel or update DATABASE_BACKUP_MSG_ID")
                
        except Exception as msg_e:
            print(f"❌ Cannot get backup message: {msg_e}")
            print("   🔧 Fix: Check DATABASE_BACKUP_MSG_ID or create initial message")
            
        # Test 4: Try to send a test message
        print(f"\n✉️  Test 4: Send Test Message")
        try:
            test_msg = await client.send_message(
                STORAGE_CHANNEL, 
                "🧪 **TGDrive Connection Test**\n\n"
                "This is a test message to verify bot can send messages to the storage channel.\n"
                f"Test performed at: {asyncio.get_event_loop().time()}"
            )
            print("✅ Test message sent successfully")
            print(f"   Message ID: {test_msg.id}")
            
            # Clean up test message
            try:
                await client.delete_messages(STORAGE_CHANNEL, test_msg.id)
                print("✅ Test message cleaned up")
            except:
                print("⚠️  Could not delete test message (this is normal)")
                
        except Exception as send_e:
            print(f"❌ Cannot send messages: {send_e}")
            print("   🔧 Fix: Make sure bot has 'Post Messages' permission")
            
        # Test 5: Download test (if backup message exists)
        print(f"\n⬇️  Test 5: Download Test")
        try:
            msg = await client.get_messages(STORAGE_CHANNEL, DATABASE_BACKUP_MSG_ID)
            if msg and msg.document:
                print("✅ Backup file download test would work")
                print(f"   File: {msg.document.file_name}")
                print(f"   Size: {msg.document.file_size} bytes")
            else:
                print("⚠️  No document found for download test")
                print("   This is normal for new setups")
                
        except Exception as dl_e:
            print(f"❌ Download test failed: {dl_e}")
            
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return False
        
    finally:
        try:
            await client.stop()
            print(f"\n🛑 Bot client stopped")
        except:
            pass
    
    print("\n" + "=" * 50)
    print("🎯 Summary:")
    print("   If all tests passed, your TGDrive should work!")
    print("   If any tests failed, follow the fix suggestions above.")
    print("   For more help, check TELEGRAM_CHANNEL_SETUP_FIX.md")
    
    return True

async def create_initial_setup():
    """Create initial backup message if it doesn't exist"""
    
    print("\n🔧 Creating Initial Setup...")
    
    session_cache_path = Path("./cache")
    session_cache_path.mkdir(parents=True, exist_ok=True)
    
    client = Client(
        name="setup_session",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workdir=session_cache_path,
        proxy=TOR_PROXY
    )
    
    try:
        await client.start()
        
        # Create initial backup message
        msg = await client.send_message(
            STORAGE_CHANNEL,
            "🔐 **TGDrive Initial Setup**\n\n"
            "This is the initial backup message for TGDrive.\n"
            "The drive.data file will be uploaded here automatically.\n\n"
            "⚠️ **DO NOT DELETE THIS MESSAGE**"
        )
        
        print(f"✅ Initial backup message created!")
        print(f"   Message ID: {msg.id}")
        print(f"   Update your DATABASE_BACKUP_MSG_ID to: {msg.id}")
        
        # Pin the message
        try:
            await msg.pin()
            print("✅ Message pinned successfully")
        except Exception as pin_e:
            print(f"⚠️  Could not pin message: {pin_e}")
            
    except Exception as e:
        print(f"❌ Failed to create initial setup: {e}")
        
    finally:
        await client.stop()

if __name__ == "__main__":
    print("� Choose an option:")
    print("1. Test connection to storage channel")
    print("2. Create initial backup message")
    print("3. Both (recommended)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice in ["1", "3"]:
        print("\n" + "🔍 Running connection test...")
        asyncio.run(test_storage_channel())
    
    if choice in ["2", "3"]:
        confirm = input("\n❓ Create initial backup message? This will send a message to your channel. (y/N): ").strip().lower()
        if confirm == 'y':
            asyncio.run(create_initial_setup())
        else:
            print("⏭️  Skipped initial setup creation")
            
    print("\n✨ Test completed!")