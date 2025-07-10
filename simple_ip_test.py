#!/usr/bin/env python3
"""
Simple IP and connectivity test for TGDrive
This script tests basic connectivity without requiring additional packages
"""

import socket
import urllib.request
import urllib.error
import json
import sys

def test_basic_connectivity():
    """Test basic internet connectivity"""
    print("🌐 Testing Basic Internet Connectivity")
    print("=" * 40)
    
    # Test 1: DNS Resolution
    try:
        socket.gethostbyname('google.com')
        print("✅ DNS resolution works")
    except socket.gaierror:
        print("❌ DNS resolution failed")
        return False
    
    # Test 2: HTTP connectivity
    try:
        urllib.request.urlopen('http://google.com', timeout=10)
        print("✅ HTTP connectivity works")
    except:
        print("❌ HTTP connectivity failed")
        return False
    
    # Test 3: HTTPS connectivity  
    try:
        urllib.request.urlopen('https://google.com', timeout=10)
        print("✅ HTTPS connectivity works")
    except:
        print("❌ HTTPS connectivity failed")
        return False
    
    return True

def test_telegram_connectivity():
    """Test connectivity to Telegram servers"""
    print("\n📱 Testing Telegram Connectivity")
    print("=" * 40)
    
    telegram_endpoints = [
        'api.telegram.org',
        'core.telegram.org', 
        '149.154.167.50',  # Telegram server IP
        '149.154.175.50'   # Another Telegram server IP
    ]
    
    for endpoint in telegram_endpoints:
        try:
            if endpoint.replace('.', '').isdigit() or ':' in endpoint:
                # IP address
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                result = sock.connect_ex((endpoint, 443))
                sock.close()
                if result == 0:
                    print(f"✅ Can connect to {endpoint}:443")
                else:
                    print(f"❌ Cannot connect to {endpoint}:443")
            else:
                # Domain name
                socket.gethostbyname(endpoint)
                print(f"✅ Can resolve {endpoint}")
        except Exception as e:
            print(f"❌ Failed to connect to {endpoint}: {e}")

def get_ip_info():
    """Get current IP information"""
    print("\n🔍 IP Information")
    print("=" * 40)
    
    try:
        # Get external IP
        response = urllib.request.urlopen('https://api.ipify.org?format=json', timeout=10)
        data = json.loads(response.read().decode())
        external_ip = data['ip']
        print(f"📍 External IP: {external_ip}")
        
        # Get IP geolocation info
        try:
            response = urllib.request.urlopen(f'http://ip-api.com/json/{external_ip}', timeout=10)
            geo_data = json.loads(response.read().decode())
            print(f"🌍 Location: {geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}")
            print(f"🏢 ISP: {geo_data.get('isp', 'Unknown')}")
            print(f"🏗️  Organization: {geo_data.get('org', 'Unknown')}")
            
            # Check if it's a VPS/hosting provider
            org = geo_data.get('org', '').lower()
            isp = geo_data.get('isp', '').lower()
            hosting_keywords = ['digital ocean', 'amazon', 'google cloud', 'vultr', 'linode', 'hetzner', 'ovh', 'contabo']
            
            is_hosting = any(keyword in org or keyword in isp for keyword in hosting_keywords)
            if is_hosting:
                print("⚠️  This appears to be a VPS/Cloud hosting IP")
                print("   Some VPS IPs are blocked by Telegram")
            else:
                print("✅ This appears to be a residential/ISP IP")
                
        except Exception as e:
            print(f"⚠️  Could not get geolocation info: {e}")
            
    except Exception as e:
        print(f"❌ Could not get IP info: {e}")

def test_tor_connectivity():
    """Test if Tor is running and accessible"""
    print("\n🔐 Testing Tor Connectivity")
    print("=" * 40)
    
    try:
        # Test if Tor SOCKS proxy is running
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('127.0.0.1', 9050))
        sock.close()
        
        if result == 0:
            print("✅ Tor proxy is running on 127.0.0.1:9050")
        else:
            print("❌ Tor proxy is NOT running on 127.0.0.1:9050")
            print("   Your application is configured to use Tor but it's not available")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Tor: {e}")
        return False
    
    return True

def test_telegram_bot_api():
    """Test Telegram Bot API accessibility"""
    print("\n🤖 Testing Telegram Bot API")
    print("=" * 40)
    
    # Updated bot token
    bot_token = "7934604269:AAHNUA-tKN0zjJ0wY1ZOfvQCeFNakY97BNE"
    
    try:
        # Test getMe endpoint
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = urllib.request.urlopen(url, timeout=15)
        data = json.loads(response.read().decode())
        
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Bot API accessible")
            print(f"   Bot Username: @{bot_info.get('username')}")
            print(f"   Bot Name: {bot_info.get('first_name')}")
            return True
        else:
            print(f"❌ Bot API error: {data.get('description')}")
            return False
            
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Bot token is invalid (401 Unauthorized)")
        elif e.code == 403:
            print("❌ Bot token is forbidden (403 Forbidden)")
        else:
            print(f"❌ HTTP error {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ Cannot reach Telegram Bot API: {e}")
        print("   This might indicate IP blocking by Telegram")
        return False

def main():
    print("🔧 TGDrive IP & Connectivity Diagnostic Tool")
    print("=" * 50)
    print()
    
    # Test 1: Basic connectivity
    if not test_basic_connectivity():
        print("\n❌ Basic connectivity failed. Check your internet connection.")
        return
    
    # Test 2: Get IP info
    get_ip_info()
    
    # Test 3: Telegram connectivity
    test_telegram_connectivity()
    
    # Test 4: Tor connectivity
    tor_available = test_tor_connectivity()
    
    # Test 5: Telegram Bot API
    bot_api_works = test_telegram_bot_api()
    
    # Summary and recommendations
    print("\n" + "=" * 50)
    print("🎯 DIAGNOSIS & RECOMMENDATIONS")
    print("=" * 50)
    
    if not bot_api_works:
        print("❌ MAIN ISSUE: Cannot access Telegram Bot API")
        print("\n🔧 SOLUTIONS:")
        print("1. Your IP might be blocked by Telegram")
        print("2. Try using a VPN or different server")
        print("3. Contact your VPS provider about Telegram access")
        if not tor_available:
            print("4. Install and configure Tor proxy:")
            print("   sudo apt update && sudo apt install tor")
            print("   sudo systemctl start tor")
            print("   sudo systemctl enable tor")
        else:
            print("4. Tor is available but might not be working with Telegram")
    else:
        print("✅ Bot API is accessible")
        print("\n🔧 Your 'Peer id invalid' error is likely due to:")
        print("1. NEW BOT not added to the storage channel as admin")
        print("2. Incorrect channel ID")
        print("3. Channel doesn't exist or was deleted")
        print("4. DATABASE_BACKUP_MSG_ID points to non-existent message")
        
        print("\n📋 NEXT STEPS:")
        print("1. Check your storage channel -1002843656111")
        print("2. REMOVE old bot and ADD NEW BOT as admin in that channel")
        print("3. Verify message ID 10 exists in the channel")
        print("4. Or create a new channel and update your config")

if __name__ == "__main__":
    main()