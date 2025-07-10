#!/usr/bin/env python3
"""
Script untuk update bot token baru di .env file
"""

import os
import sys

def update_bot_token():
    print("🤖 TGDrive Bot Token Updater")
    print("=" * 40)
    
    # Get new token from user
    if len(sys.argv) > 1:
        new_token = sys.argv[1]
    else:
        print("Usage: python3 update_bot_token.py <NEW_BOT_TOKEN>")
        print("Example: python3 update_bot_token.py 7123456789:AAGxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("\nOr run without arguments for interactive mode:")
        new_token = input("\n🔑 Enter new bot token: ").strip()
    
    if not new_token or ":" not in new_token:
        print("❌ Invalid token format!")
        print("Token should be like: 7123456789:AAGxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        return
    
    # Read current .env
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"❌ {env_file} not found!")
        return
    
    with open(env_file, "r") as f:
        lines = f.readlines()
    
    # Update tokens
    updated_lines = []
    updated_count = 0
    
    for line in lines:
        if line.startswith("BOT_TOKENS="):
            updated_lines.append(f"BOT_TOKENS={new_token}\n")
            updated_count += 1
            print(f"✅ Updated BOT_TOKENS")
        elif line.startswith("MAIN_BOT_TOKEN="):
            updated_lines.append(f"MAIN_BOT_TOKEN={new_token}\n")
            updated_count += 1
            print(f"✅ Updated MAIN_BOT_TOKEN")
        else:
            updated_lines.append(line)
    
    # Write back to file
    with open(env_file, "w") as f:
        f.writelines(updated_lines)
    
    print(f"\n🎉 Successfully updated {updated_count} token entries!")
    print(f"📄 File: {env_file}")
    
    # Test new token
    print(f"\n🔍 Testing new token...")
    bot_id = new_token.split(":")[0]
    print(f"   Bot ID: {bot_id}")
    
    print(f"\n📋 Next steps:")
    print(f"   1. Add new bot to channel -1002678381463 as admin")
    print(f"   2. Clear cache: rm -rf cache/")
    print(f"   3. Start TGDrive: python3 -m uvicorn main:app --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    update_bot_token()