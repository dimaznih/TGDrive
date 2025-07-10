#!/usr/bin/env python3
"""
Shared Communication System for TGDrive
Handles communication between Bot Service and Web Service
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional
from utils.logger import Logger

logger = Logger(__name__)

# Shared directory for communication
SHARED_DIR = Path("./shared")
SHARED_DIR.mkdir(exist_ok=True)

class SharedCommunication:
    def __init__(self):
        self.bot_status_file = SHARED_DIR / "bot_status.json"
        self.drive_sync_file = SHARED_DIR / "drive_sync.json"
        self.commands_file = SHARED_DIR / "commands.json"
        self.web_status_file = SHARED_DIR / "web_status.json"
        
    def write_json(self, filepath: Path, data: Dict[str, Any]) -> None:
        """Safely write JSON data to file"""
        try:
            temp_file = filepath.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
            temp_file.replace(filepath)  # Atomic operation
        except Exception as e:
            logger.error(f"Error writing to {filepath}: {e}")
    
    def read_json(self, filepath: Path) -> Dict[str, Any]:
        """Safely read JSON data from file"""
        try:
            if filepath.exists():
                with open(filepath, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error reading from {filepath}: {e}")
            return {}
    
    # Bot Status Methods
    def update_bot_status(self, status: str, details: Optional[Dict] = None) -> None:
        """Update bot service status"""
        data = {
            "status": status,  # "starting", "running", "stopped", "error"
            "timestamp": time.time(),
            "details": details or {},
            "clients_count": details.get("clients_count", 0) if details else 0
        }
        self.write_json(self.bot_status_file, data)
        logger.info(f"Bot status updated: {status}")
    
    def get_bot_status(self) -> Dict[str, Any]:
        """Get current bot service status"""
        return self.read_json(self.bot_status_file)
    
    def is_bot_running(self) -> bool:
        """Check if bot service is running"""
        status = self.get_bot_status()
        return status.get("status") == "running"
    
    # Web Status Methods  
    def update_web_status(self, status: str, details: Optional[Dict] = None) -> None:
        """Update web service status"""
        data = {
            "status": status,  # "starting", "running", "stopped", "error"
            "timestamp": time.time(),
            "details": details or {},
            "port": details.get("port", 8000) if details else 8000
        }
        self.write_json(self.web_status_file, data)
        logger.info(f"Web status updated: {status}")
    
    def get_web_status(self) -> Dict[str, Any]:
        """Get current web service status"""
        return self.read_json(self.web_status_file)
    
    # Drive Data Sync Methods
    def update_drive_sync(self, data: Dict[str, Any]) -> None:
        """Update drive data sync status"""
        sync_data = {
            "last_sync": time.time(),
            "drive_data": data,
            "version": data.get("version", 1)
        }
        self.write_json(self.drive_sync_file, sync_data)
    
    def get_drive_data(self) -> Dict[str, Any]:
        """Get synced drive data"""
        sync_data = self.read_json(self.drive_sync_file)
        return sync_data.get("drive_data", {})
    
    def get_last_sync_time(self) -> float:
        """Get last sync timestamp"""
        sync_data = self.read_json(self.drive_sync_file)
        return sync_data.get("last_sync", 0)
    
    # Command Methods (Web -> Bot communication)
    def send_command(self, command: str, params: Optional[Dict] = None) -> None:
        """Send command from web to bot"""
        commands = self.read_json(self.commands_file)
        command_id = f"{command}_{int(time.time() * 1000)}"
        
        commands[command_id] = {
            "command": command,
            "params": params or {},
            "timestamp": time.time(),
            "status": "pending"  # "pending", "processing", "completed", "failed"
        }
        
        self.write_json(self.commands_file, commands)
        logger.info(f"Command sent: {command}")
    
    def get_pending_commands(self) -> Dict[str, Any]:
        """Get pending commands for bot to process"""
        commands = self.read_json(self.commands_file)
        return {k: v for k, v in commands.items() if v.get("status") == "pending"}
    
    def update_command_status(self, command_id: str, status: str, result: Optional[Dict] = None) -> None:
        """Update command processing status"""
        commands = self.read_json(self.commands_file)
        if command_id in commands:
            commands[command_id]["status"] = status
            commands[command_id]["updated"] = time.time()
            if result:
                commands[command_id]["result"] = result
            self.write_json(self.commands_file, commands)
    
    def cleanup_old_commands(self, max_age_hours: int = 24) -> None:
        """Clean up old commands"""
        commands = self.read_json(self.commands_file)
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        cleaned_commands = {
            k: v for k, v in commands.items()
            if (current_time - v.get("timestamp", 0)) < max_age_seconds
        }
        
        if len(cleaned_commands) != len(commands):
            self.write_json(self.commands_file, cleaned_commands)
            logger.info(f"Cleaned up {len(commands) - len(cleaned_commands)} old commands")
    
    # Health Check Methods
    def health_check(self) -> Dict[str, Any]:
        """Overall system health check"""
        bot_status = self.get_bot_status()
        web_status = self.get_web_status()
        last_sync = self.get_last_sync_time()
        
        current_time = time.time()
        
        return {
            "bot_healthy": (
                bot_status.get("status") == "running" and 
                (current_time - bot_status.get("timestamp", 0)) < 60
            ),
            "web_healthy": (
                web_status.get("status") == "running" and
                (current_time - web_status.get("timestamp", 0)) < 60  
            ),
            "sync_recent": (current_time - last_sync) < 300,  # 5 minutes
            "bot_status": bot_status,
            "web_status": web_status,
            "last_sync": last_sync
        }

# Global instance
shared_comm = SharedCommunication()