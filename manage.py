#!/usr/bin/env python3
"""
TGDrive Service Manager
Manages Bot Service and Web Service independently
"""

import subprocess
import sys
import time
import signal
import argparse
from pathlib import Path
from utils.shared_comm import shared_comm
from utils.logger import Logger

logger = Logger(__name__)

class ServiceManager:
    def __init__(self):
        self.bot_process = None
        self.web_process = None
        self.pid_dir = Path("./pids")
        self.pid_dir.mkdir(exist_ok=True)
        self.bot_pid_file = self.pid_dir / "bot.pid"
        self.web_pid_file = self.pid_dir / "web.pid"
    
    def start_bot(self):
        """Start bot service"""
        if self.is_bot_running():
            print("❌ Bot service is already running")
            return False
        
        print("🤖 Starting Bot Service...")
        try:
            self.bot_process = subprocess.Popen([
                sys.executable, "bot_service.py"
            ], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
            )
            
            # Save PID
            with open(self.bot_pid_file, 'w') as f:
                f.write(str(self.bot_process.pid))
            
            # Wait a moment to see if it starts successfully
            time.sleep(3)
            
            if self.bot_process.poll() is None:  # Still running
                print(f"✅ Bot Service started (PID: {self.bot_process.pid})")
                return True
            else:
                print("❌ Bot Service failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start bot service: {e}")
            return False
    
    def start_web(self, host="0.0.0.0", port=8000):
        """Start web service"""
        if self.is_web_running():
            print("❌ Web service is already running")
            return False
        
        print(f"🌐 Starting Web Service on {host}:{port}...")
        try:
            self.web_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", host, "--port", str(port)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
            )
            
            # Save PID
            with open(self.web_pid_file, 'w') as f:
                f.write(str(self.web_process.pid))
            
            # Wait a moment to see if it starts successfully
            time.sleep(3)
            
            if self.web_process.poll() is None:  # Still running
                print(f"✅ Web Service started (PID: {self.web_process.pid})")
                return True
            else:
                print("❌ Web Service failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start web service: {e}")
            return False
    
    def stop_bot(self):
        """Stop bot service"""
        pid = self.get_bot_pid()
        if not pid:
            print("❌ Bot service is not running")
            return False
        
        print(f"🛑 Stopping Bot Service (PID: {pid})...")
        try:
            subprocess.run(["kill", "-TERM", str(pid)], check=True)
            time.sleep(2)
            
            # Check if process still exists
            try:
                subprocess.run(["kill", "-0", str(pid)], check=True)
                # Still running, force kill
                subprocess.run(["kill", "-KILL", str(pid)], check=True)
                print("🔥 Force killed bot service")
            except subprocess.CalledProcessError:
                # Process is gone
                pass
            
            # Remove PID file
            if self.bot_pid_file.exists():
                self.bot_pid_file.unlink()
            
            print("✅ Bot Service stopped")
            return True
            
        except Exception as e:
            print(f"❌ Failed to stop bot service: {e}")
            return False
    
    def stop_web(self):
        """Stop web service"""
        pid = self.get_web_pid()
        if not pid:
            print("❌ Web service is not running")
            return False
        
        print(f"🛑 Stopping Web Service (PID: {pid})...")
        try:
            subprocess.run(["kill", "-TERM", str(pid)], check=True)
            time.sleep(2)
            
            # Check if process still exists
            try:
                subprocess.run(["kill", "-0", str(pid)], check=True)
                # Still running, force kill
                subprocess.run(["kill", "-KILL", str(pid)], check=True)
                print("🔥 Force killed web service")
            except subprocess.CalledProcessError:
                # Process is gone
                pass
            
            # Remove PID file
            if self.web_pid_file.exists():
                self.web_pid_file.unlink()
            
            print("✅ Web Service stopped")
            return True
            
        except Exception as e:
            print(f"❌ Failed to stop web service: {e}")
            return False
    
    def get_bot_pid(self):
        """Get bot service PID"""
        try:
            if self.bot_pid_file.exists():
                with open(self.bot_pid_file, 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return None
    
    def get_web_pid(self):
        """Get web service PID"""
        try:
            if self.web_pid_file.exists():
                with open(self.web_pid_file, 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return None
    
    def is_bot_running(self):
        """Check if bot service is running"""
        pid = self.get_bot_pid()
        if not pid:
            return False
        
        try:
            subprocess.run(["kill", "-0", str(pid)], check=True)
            return True
        except subprocess.CalledProcessError:
            # Process doesn't exist, remove stale PID file
            if self.bot_pid_file.exists():
                self.bot_pid_file.unlink()
            return False
    
    def is_web_running(self):
        """Check if web service is running"""
        pid = self.get_web_pid()
        if not pid:
            return False
        
        try:
            subprocess.run(["kill", "-0", str(pid)], check=True)
            return True
        except subprocess.CalledProcessError:
            # Process doesn't exist, remove stale PID file
            if self.web_pid_file.exists():
                self.web_pid_file.unlink()
            return False
    
    def status(self):
        """Show service status"""
        print("📊 TGDrive Service Status")
        print("=" * 40)
        
        # Bot service status
        bot_running = self.is_bot_running()
        bot_pid = self.get_bot_pid()
        bot_status = shared_comm.get_bot_status()
        
        print(f"🤖 Bot Service: {'🟢 RUNNING' if bot_running else '🔴 STOPPED'}")
        if bot_running and bot_pid:
            print(f"   PID: {bot_pid}")
        if bot_status:
            print(f"   Status: {bot_status.get('status', 'unknown')}")
            print(f"   Clients: {bot_status.get('clients_count', 0)}")
        
        # Web service status
        web_running = self.is_web_running()
        web_pid = self.get_web_pid()
        web_status = shared_comm.get_web_status()
        
        print(f"🌐 Web Service: {'🟢 RUNNING' if web_running else '🔴 STOPPED'}")
        if web_running and web_pid:
            print(f"   PID: {web_pid}")
        if web_status:
            print(f"   Status: {web_status.get('status', 'unknown')}")
            print(f"   Port: {web_status.get('details', {}).get('port', 'unknown')}")
        
        # Health check
        health = shared_comm.health_check()
        print(f"\n🏥 Overall Health: {'🟢 HEALTHY' if health.get('bot_healthy') and health.get('web_healthy') else '⚠️ DEGRADED'}")
        
    def restart_bot(self):
        """Restart bot service"""
        print("🔄 Restarting Bot Service...")
        self.stop_bot()
        time.sleep(2)
        return self.start_bot()
    
    def restart_web(self, host="0.0.0.0", port=8000):
        """Restart web service"""
        print("🔄 Restarting Web Service...")
        self.stop_web()
        time.sleep(2)
        return self.start_web(host, port)
    
    def start_all(self, host="0.0.0.0", port=8000):
        """Start both services"""
        print("🚀 Starting All Services...")
        bot_success = self.start_bot()
        time.sleep(3)  # Give bot time to initialize
        web_success = self.start_web(host, port)
        
        if bot_success and web_success:
            print("🎉 All services started successfully!")
            return True
        else:
            print("❌ Some services failed to start")
            return False
    
    def stop_all(self):
        """Stop both services"""
        print("🛑 Stopping All Services...")
        web_success = self.stop_web()
        bot_success = self.stop_bot()
        
        if bot_success and web_success:
            print("✅ All services stopped successfully!")
            return True
        else:
            print("⚠️ Some services may still be running")
            return False

def main():
    parser = argparse.ArgumentParser(description="TGDrive Service Manager")
    parser.add_argument("action", choices=[
        "start-bot", "stop-bot", "restart-bot",
        "start-web", "stop-web", "restart-web", 
        "start-all", "stop-all", "status"
    ], help="Action to perform")
    parser.add_argument("--host", default="0.0.0.0", help="Web service host")
    parser.add_argument("--port", default=8000, type=int, help="Web service port")
    
    args = parser.parse_args()
    manager = ServiceManager()
    
    if args.action == "start-bot":
        manager.start_bot()
    elif args.action == "stop-bot":
        manager.stop_bot()
    elif args.action == "restart-bot":
        manager.restart_bot()
    elif args.action == "start-web":
        manager.start_web(args.host, args.port)
    elif args.action == "stop-web":
        manager.stop_web()
    elif args.action == "restart-web":
        manager.restart_web(args.host, args.port)
    elif args.action == "start-all":
        manager.start_all(args.host, args.port)
    elif args.action == "stop-all":
        manager.stop_all()
    elif args.action == "status":
        manager.status()

if __name__ == "__main__":
    main()