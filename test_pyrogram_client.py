#!/usr/bin/env python3
"""
Test pyrogram client access like the actual TGDrive application
"""

import asyncio
import config
from pyrogram import Client
from pathlib import Path

# TOR PROXY CONFIG (same as clients.py)
TOR_PROXY = {
    "scheme": "socks5",
    "hostname": "127.0.0.1", 
    "port": 9050
}

async def test_pyrogram_client():
    print("🔧 Test Pyrogram Client Access")
    print("=" * 50)
    
    session_cache_path = Path("./cache")
    session_cache_path.mkdir(parents=True, exist_ok=True)
    
    client = None
    try:
        print("📡 Creating pyrogram client...")
        client = Client(
            name="test_client",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.MAIN_BOT_TOKEN,
            workdir=session_cache_path,
            proxy=TOR_PROXY
        )
        
        print("🚀 Starting client...")
        await client.start()
        print("✅ Client started successfully!")
        
        print(f"\n📋 Testing channel access: {config.STORAGE_CHANNEL}")
        print(f"📋 Testing message ID: {config.DATABASE_BACKUP_MSG_ID}")
        
        # Test 1: Get chat info
        try:
            chat = await client.get_chat(config.STORAGE_CHANNEL)
            print(f"✅ Chat found: {chat.title} ({chat.type})")
        except Exception as e:
            print(f"❌ Get chat failed: {e}")
            return False
        
        # Test 2: Get specific message (like in loadDriveData)
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
            print("   This is the exact error TGDrive encounters!")
            return False
        
        # Test 3: Send a test message
        try:
            test_msg = await client.send_message(
                config.STORAGE_CHANNEL,
                "🧪 Test message from Pyrogram client"
            )
            print(f"✅ Test message sent successfully! ID: {test_msg.id}")
            
            # Try to delete test message to keep channel clean
            try:
                await client.delete_messages(config.STORAGE_CHANNEL, test_msg.id)
                print("🗑️  Test message deleted")
            except:
                pass
                
        except Exception as e:
            print(f"❌ Send message failed: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎯 RESULT: Pyrogram client test SUCCESSFUL! ✅")
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
        result = asyncio.run(test_pyrogram_client())
        if result:
            print("\n✅ Pyrogram client works fine!")
            print("💡 The issue might be elsewhere...")
        else:
            print("\n❌ Pyrogram client has issues!")
            print("💡 This explains why TGDrive fails!")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")