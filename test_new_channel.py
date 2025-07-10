#!/usr/bin/env python3
"""
Test akses ke channel baru untuk TGDrive
"""

import urllib.request
import urllib.error
import urllib.parse
import json

def test_new_channel():
    print("🔧 Test Channel Fresh TGDrive")
    print("=" * 40)
    
    # Konfigurasi fresh
    bot_token = "7079298713:AAGZM6gAkH7EUuqP8uTdY9lhLcua-ApAXWM"
    new_channel = -1002678381463
    message_id = 10
    
    print(f"🤖 Bot: New Fresh Bot")
    print(f"📡 Channel: {new_channel}")
    print(f"📄 Message ID: {message_id}")
    print()
    
    # Test 1: Bot info
    try:
        print("📋 Test 1: Bot Information")
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = urllib.request.urlopen(url, timeout=15)
        data = json.loads(response.read().decode())
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"   ✅ Bot: @{bot_info.get('username')} ({bot_info.get('first_name')})")
        else:
            print(f"   ❌ Bot error: {data.get('description')}")
            return False
    except Exception as e:
        print(f"   ❌ Bot test failed: {e}")
        return False
    
    # Test 2: Channel access
    try:
        print("\n📡 Test 2: Channel Access")
        url = f"https://api.telegram.org/bot{bot_token}/getChat"
        data = urllib.parse.urlencode({'chat_id': new_channel}).encode()
        request = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(request, timeout=15)
        result = json.loads(response.read().decode())
        
        if result.get('ok'):
            chat_info = result['result']
            print(f"   ✅ Channel found: {chat_info.get('title', 'Unknown')}")
            print(f"   📋 Type: {chat_info.get('type', 'Unknown')}")
        else:
            print(f"   ❌ Channel access failed: {result.get('description')}")
            return False
    except Exception as e:
        print(f"   ❌ Channel test failed: {e}")
        return False
    
    # Test 3: Message access (optional)
    try:
        print("\n📄 Test 3: Message Access")
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = urllib.request.urlopen(url, timeout=15)
        data = json.loads(response.read().decode())
        
        if data.get('ok'):
            print(f"   ✅ Can get updates from bot")
        else:
            print(f"   ⚠️  Updates warning: {data.get('description')}")
            
    except Exception as e:
        print(f"   ⚠️  Message test warning: {e}")
    
    # Test 4: Check specific message
    try:
        print(f"\n📄 Test 4: Check Message ID {message_id}")
        url = f"https://api.telegram.org/bot{bot_token}/forwardMessage"
        data = urllib.parse.urlencode({
            'chat_id': new_channel,
            'from_chat_id': new_channel,
            'message_id': message_id
        }).encode()
        
        request = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(request, timeout=15)
        result = json.loads(response.read().decode())
        
        if result.get('ok'):
            print(f"   ✅ Message {message_id} exists and accessible!")
        else:
            print(f"   ❌ Message {message_id} not found: {result.get('description')}")
            print(f"   � Will try to send a new backup message...")
            
            # Send backup message
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            message_text = "🔐 TGDrive Database Backup\n\nIni adalah backup file untuk TGDrive.\nJANGAN HAPUS MESSAGE INI!"
            data = urllib.parse.urlencode({
                'chat_id': new_channel,
                'text': message_text
            }).encode()
            
            request = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(request, timeout=15)
            result = json.loads(response.read().decode())
            
            if result.get('ok'):
                new_msg_id = result['result']['message_id']
                print(f"   ✅ New backup message created with ID: {new_msg_id}")
                print(f"   💡 RECOMMENDED: Update DATABASE_BACKUP_MSG_ID={new_msg_id}")
                return True
            else:
                print(f"   ❌ Failed to create backup message: {result.get('description')}")
                return False
            
    except Exception as e:
        print(f"   ❌ Message check failed: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎯 RESULT: Fresh channel READY! ✅")
    print("🚀 Sekarang jalankan aplikasi TGDrive")
    return True

if __name__ == "__main__":
    if test_new_channel():
        print("\n📋 Next steps:")
        print("1. rm -rf cache/")
        print("2. uvicorn main:app --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Channel setup belum sempurna, cek konfigurasi lagi")