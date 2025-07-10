#!/usr/bin/env python3
"""
🔧 TGDrive Bot & Channel Test Script - Updated Token
Tests bot connection and channel access
"""

import asyncio
import config
from pyrogram import Client
import traceback

# Use Tor proxy for testing
TOR_PROXY = {
    "scheme": "socks5",
    "hostname": "127.0.0.1", 
    "port": 9050
}

async def test_bot_connection():
    print("🔍 Testing TGDrive Bot Connection...")
    print(f"📋 Bot Token: {config.BOT_TOKENS[0][:20]}...")
    print(f"📋 Channel ID: {config.STORAGE_CHANNEL}")
    print(f"📋 Using Tor Proxy: {TOR_PROXY['hostname']}:{TOR_PROXY['port']}")
    print("-" * 50)
    
    try:
        # Create bot client with proxy
        bot = Client(
            name="test_bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKENS[0],
            proxy=TOR_PROXY,
            workdir="./cache/"
        )
        
        print("🤝 Starting bot...")
        await bot.start()
        print("✅ Bot connected successfully!")
        
        # Get bot info
        me = await bot.get_me()
        print(f"📱 Bot Name: {me.first_name}")
        print(f"📱 Bot Username: @{me.username}")
        
        # Test channel access
        print(f"\n🔍 Testing channel access: {config.STORAGE_CHANNEL}")
        try:
            chat = await bot.get_chat(config.STORAGE_CHANNEL)
            print(f"✅ Channel found: {chat.title}")
            print(f"� Channel Type: {chat.type}")
            
            # Check bot permissions
            try:
                member = await bot.get_chat_member(config.STORAGE_CHANNEL, me.id)
                print(f"🔑 Bot Status: {member.status}")
                
                if str(member.status) in ['ChatMemberStatus.ADMINISTRATOR', 'ChatMemberStatus.CREATOR']:
                    print("✅ Bot has admin permissions")
                    
                    # Try to send a test message
                    try:
                        test_msg = await bot.send_message(
                            config.STORAGE_CHANNEL, 
                            "🧪 Test message from TGDrive setup - NEW TOKEN"
                        )
                        print("✅ Successfully sent test message")
                        
                        # Delete test message
                        await bot.delete_messages(config.STORAGE_CHANNEL, test_msg.id)
                        print("✅ Test message deleted")
                        
                    except Exception as e:
                        print(f"❌ Failed to send message: {e}")
                else:
                    print(f"❌ Bot is not admin! Status: {member.status}")
                    
            except Exception as e:
                print(f"❌ Failed to get member info: {e}")
                
        except Exception as e:
            print(f"❌ Failed to access channel: {e}")
            print("💡 Possible issues:")
            print("   - Bot not added to channel")
            print("   - Channel ID incorrect") 
            print("   - Bot not admin in channel")
        
        await bot.stop()
        print("\n� Test completed!")
        
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        print(f"📋 Full error: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(test_bot_connection())