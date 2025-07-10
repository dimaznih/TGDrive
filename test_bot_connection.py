#!/usr/bin/env python3
"""
🔧 TGDrive Bot & Channel Test Script
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
            in_memory=True
        )
        
        print("🚀 Starting bot...")
        await bot.start()
        print("✅ Bot connected successfully!")
        
        # Get bot info
        me = await bot.get_me()
        print(f"🤖 Bot Info: @{me.username} ({me.first_name})")
        
        # Test channel access
        print(f"\n🔍 Testing channel access: {config.STORAGE_CHANNEL}")
        try:
            chat = await bot.get_chat(config.STORAGE_CHANNEL)
            print(f"✅ Channel found: {chat.title}")
            print(f"📋 Type: {chat.type}")
            print(f"📋 Members: {chat.members_count if hasattr(chat, 'members_count') else 'Unknown'}")
            
            # Check bot permissions
            try:
                member = await bot.get_chat_member(config.STORAGE_CHANNEL, me.id)
                print(f"✅ Bot status in channel: {member.status}")
                
                if str(member.status) in ['ChatMemberStatus.ADMINISTRATOR', 'ChatMemberStatus.CREATOR']:
                    print("✅ Bot has admin permissions")
                    
                    # Check specific permissions
                    if hasattr(member, 'privileges') and member.privileges:
                        perms = member.privileges
                        print(f"📋 Permissions:")
                        print(f"   - Can post messages: {perms.can_post_messages}")
                        print(f"   - Can edit messages: {perms.can_edit_messages}")
                        print(f"   - Can delete messages: {perms.can_delete_messages}")
                        print(f"   - Can manage chat: {perms.can_manage_chat}")
                    
                    # Try to send a test message
                    try:
                        test_msg = await bot.send_message(
                            config.STORAGE_CHANNEL, 
                            "🧪 Test message from TGDrive setup"
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
                print(f"❌ Cannot get bot permissions: {e}")
                
        except Exception as e:
            print(f"❌ Cannot access channel: {e}")
            print("\n💡 SOLUTION NEEDED:")
            print("1. Make sure channel exists")
            print("2. Add bot to channel as admin")
            print("3. Send at least 1 message to channel")
            
        await bot.stop()
        print("\n🎯 Bot test completed!")
        
    except Exception as e:
        print(f"❌ Bot connection failed: {e}")
        print(f"📋 Error details: {traceback.format_exc()}")
        
        print("\n💡 TROUBLESHOOTING:")
        print("1. Verify bot token is correct")
        print("2. Check if API_ID and API_HASH are valid")
        print("3. Ensure Tor proxy is running")

if __name__ == "__main__":
    asyncio.run(test_bot_connection())