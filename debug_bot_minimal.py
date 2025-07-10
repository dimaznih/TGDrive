#!/usr/bin/env python3
"""
Minimal Bot Service for Debugging Channel Access
"""

import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

import config
from utils.logger import Logger
from pyrogram import Client

logger = Logger(__name__)

async def debug_bot_service():
    print("🔧 Debug Bot Service - Minimal Version")
    print("=" * 50)
    
    session_cache_path = Path("./cache")
    session_cache_path.mkdir(parents=True, exist_ok=True)
    
    client = None
    try:
        print("📡 Creating bot client...")
        client = Client(
            name="debug_bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.MAIN_BOT_TOKEN,
            workdir=session_cache_path,
            # No proxy - direct connection
        )
        
        print("🚀 Starting client...")
        await client.start()
        print("✅ Client started successfully!")
        
        print(f"\n📋 Testing storage channel: {config.STORAGE_CHANNEL}")
        print(f"📋 Testing message ID: {config.DATABASE_BACKUP_MSG_ID}")
        
        # Test 1: Get chat info
        try:
            chat = await client.get_chat(config.STORAGE_CHANNEL)
            print(f"✅ Chat found: {chat.title} ({chat.type})")
        except Exception as e:
            print(f"❌ Get chat failed: {e}")
            return False
        
        # Test 2: Get specific message
        try:
            msg = await client.get_messages(config.STORAGE_CHANNEL, config.DATABASE_BACKUP_MSG_ID)
            print(f"✅ Message {config.DATABASE_BACKUP_MSG_ID} found!")
            
            if msg.document:
                print(f"   📄 Document: {msg.document.file_name}")
                print(f"   📏 Size: {msg.document.file_size} bytes")
            else:
                print("   ⚠️  No document attached to message")
                
        except Exception as e:
            print(f"❌ Get messages failed: {e}")
            return False
        
        # Test 3: Simulate backup_drive_data behavior
        try:
            print(f"\n📤 Testing backup simulation...")
            
            # Create a dummy file for testing
            dummy_file = session_cache_path / "test_backup.txt"
            with open(dummy_file, 'w') as f:
                f.write("Test backup content")
            
            # Try to send/edit message (simulating backup)
            from pyrogram.types import InputMediaDocument
            
            media_doc = InputMediaDocument(
                dummy_file, 
                caption="🔐 Test Backup\n\nThis is a test backup message."
            )
            
            # Check if we can edit the message
            edited_msg = await client.edit_message_media(
                config.STORAGE_CHANNEL,
                config.DATABASE_BACKUP_MSG_ID,
                media=media_doc,
                file_name="test_backup.txt"
            )
            
            print("✅ Backup simulation successful!")
            print(f"   Message ID: {edited_msg.id}")
            
            # Clean up test file
            dummy_file.unlink()
            
        except Exception as e:
            print(f"❌ Backup simulation failed: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎯 RESULT: Minimal bot service test SUCCESSFUL! ✅")
        return True
        
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return False
        
    finally:
        if client and client.is_connected:
            await client.stop()
            print("🛑 Client stopped")

if __name__ == "__main__":
    try:
        result = asyncio.run(debug_bot_service())
        if result:
            print("\n✅ Debugging completed successfully!")
            print("💡 Bot service should work fine...")
        else:
            print("\n❌ Debugging found issues!")
            print("💡 Need to fix channel access...")
    except Exception as e:
        print(f"\n💥 Debug failed with error: {e}")