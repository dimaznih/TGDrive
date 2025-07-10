#!/usr/bin/env python3
"""
Script untuk cek sisa waktu flood wait
"""

import time
import asyncio
from pyrogram import Client
import config
from pathlib import Path

async def check_flood_wait():
    print("🕐 Checking Flood Wait Status...")
    print("=" * 50)
    
    session_cache_path = Path("./cache")
    session_cache_path.mkdir(parents=True, exist_ok=True)
    
    try:
        client = Client(
            name="flood_check",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.MAIN_BOT_TOKEN,
            workdir=session_cache_path,
            proxy=None  # Direct connection
        )
        
        print("🔍 Testing bot token...")
        await client.start()
        print("✅ Bot token is working! No flood wait.")
        await client.stop()
        
        print("\n🎉 Good news! You can start TGDrive now:")
        print("   python3 -m uvicorn main:app --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        error_msg = str(e)
        if "FLOOD_WAIT" in error_msg:
            import re
            wait_match = re.search(r'(\d+) seconds', error_msg)
            if wait_match:
                remaining_seconds = int(wait_match.group(1))
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60
                
                print(f"⏰ Flood wait still active!")
                print(f"   Remaining time: {minutes}m {seconds}s")
                print(f"   Estimated ready at: {time.strftime('%H:%M:%S', time.localtime(time.time() + remaining_seconds))}")
                
                print(f"\n💡 Recommendations:")
                print(f"   1. Create new bot token (fastest)")
                print(f"   2. Wait {minutes} minutes")
                print(f"   3. Use different VPS/IP")
        else:
            print(f"❌ Different error: {e}")

if __name__ == "__main__":
    asyncio.run(check_flood_wait())