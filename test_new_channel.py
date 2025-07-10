#!/usr/bin/env python3
"""
Test akses ke channel baru untuk TGDrive
"""

import urllib.request
import urllib.error
import urllib.parse
import json

def test_new_channel():
    print("🔧 Test Channel Baru TGDrive")
    print("=" * 40)
    
    # Konfigurasi baru
    bot_token = "7934604269:AAHNUA-tKN0zjJ0wY1ZOfvQCeFNakY97BNE"
    new_channel = -1002790495223
    message_id = 1
    
    print(f"🤖 Bot: @Kudobot2bot")
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
    
    # Test 4: Send test message
    try:
        print("\n✉️ Test 4: Send Test Message")
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        message_text = "🧪 Test message dari TGDrive\n\nChannel baru sudah siap!"
        data = urllib.parse.urlencode({
            'chat_id': new_channel,
            'text': message_text
        }).encode()
        
        request = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(request, timeout=15)
        result = json.loads(response.read().decode())
        
        if result.get('ok'):
            msg_info = result['result']
            print(f"   ✅ Test message sent successfully!")
            print(f"   📄 Message ID: {msg_info.get('message_id')}")
            
            # Update recommended message ID if this is not ID 1
            if msg_info.get('message_id') != 1:
                print(f"\n💡 RECOMMENDED: Update DATABASE_BACKUP_MSG_ID={msg_info.get('message_id')}")
        else:
            print(f"   ❌ Send message failed: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"   ❌ Send test failed: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎯 RESULT: Channel baru READY! ✅")
    print("🚀 Sekarang jalankan aplikasi TGDrive")
    return True

if __name__ == "__main__":
    if test_new_channel():
        print("\n📋 Next steps:")
        print("1. rm -rf cache/")
        print("2. uvicorn main:app --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Channel setup belum sempurna, cek konfigurasi lagi")