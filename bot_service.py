#!/usr/bin/env python3
"""
TGDrive Bot Service - Runs independently from Web Service
Handles all Telegram bot operations and file management
"""

import asyncio
import signal
import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

import config
from utils.logger import Logger
from utils.shared_comm import shared_comm
from utils.clients import initialize_clients, get_client
from utils.directoryHandler import loadDriveData, backup_drive_data, DRIVE_DATA, init_drive_data

logger = Logger(__name__)

class BotService:
    def __init__(self):
        self.running = False
        self.clients_initialized = False
        self.drive_loaded = False
        
    async def start(self):
        """Start the bot service"""
        logger.info("🤖 Starting TGDrive Bot Service...")
        shared_comm.update_bot_status("starting", {"message": "Initializing bot service"})
        
        try:
            # Initialize clients
            logger.info("📡 Initializing Telegram clients...")
            shared_comm.update_bot_status("starting", {"message": "Connecting to Telegram"})
            
            success = await initialize_clients()
            if not success:
                logger.error("❌ Failed to initialize clients")
                shared_comm.update_bot_status("error", {"message": "Failed to connect to Telegram"})
                return False
            
            self.clients_initialized = True
            logger.info("✅ Telegram clients initialized")
            
            # Load drive data
            logger.info("💾 Loading drive data...")
            shared_comm.update_bot_status("starting", {"message": "Loading drive data"})
            
            await loadDriveData()
            await init_drive_data()
            self.drive_loaded = True
            logger.info("✅ Drive data loaded")
            
            # Start background tasks
            asyncio.create_task(self.backup_task())
            asyncio.create_task(self.command_processor())
            asyncio.create_task(self.status_updater())
            
            self.running = True
            shared_comm.update_bot_status("running", {
                "message": "Bot service running",
                "clients_count": len(config.BOT_TOKENS)
            })
            
            logger.info("🎉 Bot Service started successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot service: {e}")
            shared_comm.update_bot_status("error", {"message": str(e)})
            return False
    
    async def backup_task(self):
        """Background task for backing up drive data"""
        logger.info("📋 Starting backup task...")
        while self.running:
            try:
                await backup_drive_data(loop=False)  # Single backup
                await asyncio.sleep(config.DATABASE_BACKUP_TIME)
            except Exception as e:
                logger.error(f"Backup task error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def command_processor(self):
        """Process commands from web service"""
        logger.info("⚙️ Starting command processor...")
        while self.running:
            try:
                # Get pending commands
                commands = shared_comm.get_pending_commands()
                
                for command_id, command_data in commands.items():
                    try:
                        command = command_data["command"]
                        params = command_data.get("params", {})
                        
                        logger.info(f"Processing command: {command}")
                        shared_comm.update_command_status(command_id, "processing")
                        
                        # Process different commands
                        result = await self.process_command(command, params)
                        
                        shared_comm.update_command_status(command_id, "completed", result)
                        logger.info(f"Command {command} completed")
                        
                    except Exception as e:
                        logger.error(f"Error processing command {command_id}: {e}")
                        shared_comm.update_command_status(command_id, "failed", {"error": str(e)})
                
                # Clean up old commands
                shared_comm.cleanup_old_commands()
                
                await asyncio.sleep(2)  # Check for commands every 2 seconds
                
            except Exception as e:
                logger.error(f"Command processor error: {e}")
                await asyncio.sleep(10)
    
    async def process_command(self, command: str, params: dict) -> dict:
        """Process individual commands"""
        global DRIVE_DATA
        
        if command == "upload_file":
            # Handle file upload
            return {"status": "upload_handled"}
            
        elif command == "create_folder":
            # Handle folder creation
            path = params.get("path", "/")
            name = params.get("name", "New Folder")
            if DRIVE_DATA:
                folder_path = DRIVE_DATA.new_folder(path, name)
                return {"status": "folder_created", "path": folder_path}
            
        elif command == "delete_item":
            # Handle item deletion
            path = params.get("path")
            if DRIVE_DATA and path:
                DRIVE_DATA.delete_file_folder(path)
                return {"status": "item_deleted", "path": path}
                
        elif command == "move_items":
            # Handle item moving
            file_ids = params.get("file_ids", [])
            destination = params.get("destination", "/")
            if DRIVE_DATA:
                moved = DRIVE_DATA.move_files(file_ids, destination)
                return {"status": "items_moved", "moved_items": moved}
        
        elif command == "sync_drive_data":
            # Sync drive data to shared storage
            if DRIVE_DATA:
                # Convert DRIVE_DATA to serializable format
                drive_dict = {
                    "contents": {},  # This would need proper serialization
                    "used_ids": DRIVE_DATA.used_ids if hasattr(DRIVE_DATA, 'used_ids') else [],
                    "timestamp": time.time()
                }
                shared_comm.update_drive_sync(drive_dict)
                return {"status": "drive_synced"}
        
        return {"status": "command_not_found"}
    
    async def status_updater(self):
        """Regularly update bot status"""
        while self.running:
            try:
                details = {
                    "clients_initialized": self.clients_initialized,
                    "drive_loaded": self.drive_loaded,
                    "clients_count": len(config.BOT_TOKENS) if self.clients_initialized else 0
                }
                shared_comm.update_bot_status("running", details)
                await asyncio.sleep(30)  # Update every 30 seconds
            except Exception as e:
                logger.error(f"Status updater error: {e}")
                await asyncio.sleep(60)
    
    async def stop(self):
        """Stop the bot service"""
        logger.info("🛑 Stopping Bot Service...")
        self.running = False
        shared_comm.update_bot_status("stopped", {"message": "Bot service stopped"})
    
    def handle_signal(self, signum, frame):
        """Handle system signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())

async def main():
    """Main entry point for bot service"""
    bot_service = BotService()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, bot_service.handle_signal)
    signal.signal(signal.SIGTERM, bot_service.handle_signal)
    
    # Start the service
    success = await bot_service.start()
    if not success:
        sys.exit(1)
    
    # Keep running
    try:
        while bot_service.running:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        await bot_service.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Bot service crashed: {e}")
        shared_comm.update_bot_status("error", {"message": f"Service crashed: {e}"})
        sys.exit(1)