#!/usr/bin/env python3
"""
TGDrive Bot Service - Fixed Version
Uses same approach as successful debug script
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
from pyrogram import Client
from utils.directoryHandler import backup_drive_data, DRIVE_DATA, init_drive_data

logger = Logger(__name__)

class BotServiceFixed:
    def __init__(self):
        self.running = False
        self.client = None
        self.drive_loaded = False
        
    async def start(self):
        """Start the bot service"""
        logger.info("🤖 Starting TGDrive Bot Service (Fixed)...")
        shared_comm.update_bot_status("starting", {"message": "Initializing bot service"})
        
        try:
            # Initialize single client (like debug script)
            logger.info("📡 Creating bot client...")
            shared_comm.update_bot_status("starting", {"message": "Connecting to Telegram"})
            
            session_cache_path = Path("./cache")
            session_cache_path.mkdir(parents=True, exist_ok=True)
            
            self.client = Client(
                name="bot_service_main",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                bot_token=config.MAIN_BOT_TOKEN,
                workdir=session_cache_path,
                # No proxy - direct connection like debug script
            )
            
            logger.info("🚀 Starting client...")
            await self.client.start()
            logger.info("✅ Bot client started successfully!")
            
            # Test channel access (like debug script)
            logger.info(f"🔍 Testing channel access: {config.STORAGE_CHANNEL}")
            try:
                chat = await self.client.get_chat(config.STORAGE_CHANNEL)
                logger.info(f"✅ Channel access confirmed: {chat.title}")
                
                # Test message access
                msg = await self.client.get_messages(config.STORAGE_CHANNEL, config.DATABASE_BACKUP_MSG_ID)
                logger.info(f"✅ Message {config.DATABASE_BACKUP_MSG_ID} accessible")
            except Exception as e:
                logger.error(f"❌ Channel access test failed: {e}")
                await self.client.stop()
                shared_comm.update_bot_status("error", {"message": f"Channel access failed: {e}"})
                return False
            
            # Load drive data with working client
            logger.info("💾 Loading drive data...")
            shared_comm.update_bot_status("starting", {"message": "Loading drive data"})
            
            await self.load_drive_data_fixed()
            
            # Initialize drive data only if DRIVE_DATA exists
            global DRIVE_DATA
            if DRIVE_DATA:
                await init_drive_data()
            
            self.drive_loaded = True
            logger.info("✅ Drive data loaded")
            
            # Start background tasks
            asyncio.create_task(self.backup_task_fixed())
            asyncio.create_task(self.command_processor())
            asyncio.create_task(self.status_updater())
            
            self.running = True
            shared_comm.update_bot_status("running", {
                "message": "Bot service running",
                "clients_count": 1
            })
            
            logger.info("🎉 Bot Service started successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot service: {e}")
            shared_comm.update_bot_status("error", {"message": str(e)})
            return False
    
    async def load_drive_data_fixed(self):
        """Load drive data using our working client"""
        global DRIVE_DATA
        from utils.directoryHandler import NewDriveData, Folder
        
        logger.info("Loading drive data with fixed client...")
        
        try:
            # Try to get backup message
            msg = await self.client.get_messages(config.STORAGE_CHANNEL, config.DATABASE_BACKUP_MSG_ID)
            
            if msg.document and msg.document.file_name == "drive.data":
                logger.info("📥 Downloading backup file...")
                dl_path = await msg.download()
                
                import dill
                with open(dl_path, "rb") as f:
                    DRIVE_DATA = dill.load(f)
                
                logger.info("✅ Drive data loaded from backup")
                
                # Clean up downloaded file
                Path(dl_path).unlink()
            else:
                raise Exception("No valid backup file found")
                
        except Exception as e:
            logger.warning(f"Backup load failed: {e}")
            logger.info("Creating new drive.data file...")
            
            # Make sure to import and set global properly
            DRIVE_DATA = NewDriveData({"/": Folder("/", "/")}, [])
            DRIVE_DATA.save()
            
            # Also update the module global
            import utils.directoryHandler
            utils.directoryHandler.DRIVE_DATA = DRIVE_DATA
            
            logger.info("✅ New drive data created")
    
    async def backup_task_fixed(self):
        """Background task for backing up drive data with working client"""
        logger.info("📋 Starting backup task...")
        backup_error_count = 0
        
        while self.running:
            try:
                global DRIVE_DATA
                if not DRIVE_DATA or not DRIVE_DATA.isUpdated:
                    await asyncio.sleep(config.DATABASE_BACKUP_TIME)
                    continue
                
                logger.info("📤 Backing up drive data...")
                
                # Create backup file
                from utils.directoryHandler import drive_cache_path, get_current_utc_time
                from pyrogram.types import InputMediaDocument
                
                time_text = f"📅 **Last Updated :** {get_current_utc_time()} (UTC +00:00)"
                caption = (
                    f"🔐 **TG Drive Data Backup File**\n\n"
                    "Do not edit or delete this message. This is a backup file for the tg drive data.\n\n"
                    f"{time_text}"
                )
                
                media_doc = InputMediaDocument(drive_cache_path, caption=caption)
                
                # Edit message with backup
                msg = await self.client.edit_message_media(
                    config.STORAGE_CHANNEL,
                    config.DATABASE_BACKUP_MSG_ID,
                    media=media_doc,
                    file_name="drive.data",
                )
                
                DRIVE_DATA.isUpdated = False
                logger.info("✅ Drive data backed up successfully")
                
                # Try to pin the message
                try:
                    await msg.pin()
                except Exception as pin_e:
                    logger.warning(f"Could not pin backup message: {pin_e}")
                
                backup_error_count = 0  # Reset error count on success
                await asyncio.sleep(config.DATABASE_BACKUP_TIME)
                
            except Exception as e:
                backup_error_count += 1
                if backup_error_count <= 3:
                    logger.error(f"Backup error: {e}")
                elif backup_error_count == 4:
                    logger.warning("Multiple backup errors, reducing log frequency...")
                
                # Exponential backoff
                wait_time = min(600, 60 * (2 ** min(backup_error_count, 4)))
                await asyncio.sleep(wait_time)
    
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
            return {"status": "upload_handled"}
            
        elif command == "create_folder":
            path = params.get("path", "/")
            name = params.get("name", "New Folder")
            if DRIVE_DATA:
                folder_path = DRIVE_DATA.new_folder(path, name)
                return {"status": "folder_created", "path": folder_path}
            
        elif command == "delete_item":
            path = params.get("path")
            if DRIVE_DATA and path:
                DRIVE_DATA.delete_file_folder(path)
                return {"status": "item_deleted", "path": path}
                
        elif command == "move_items":
            file_ids = params.get("file_ids", [])
            destination = params.get("destination", "/")
            if DRIVE_DATA:
                moved = DRIVE_DATA.move_files(file_ids, destination)
                return {"status": "items_moved", "moved_items": moved}
        
        elif command == "sync_drive_data":
            if DRIVE_DATA:
                drive_dict = {
                    "contents": {},
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
                    "client_connected": self.client and self.client.is_connected,
                    "drive_loaded": self.drive_loaded,
                    "clients_count": 1 if self.client else 0
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
        
        if self.client and self.client.is_connected:
            await self.client.stop()
            logger.info("🛑 Client disconnected")
        
        shared_comm.update_bot_status("stopped", {"message": "Bot service stopped"})
    
    def handle_signal(self, signum, frame):
        """Handle system signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        asyncio.create_task(self.stop())

async def main():
    """Main entry point for bot service"""
    bot_service = BotServiceFixed()
    
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