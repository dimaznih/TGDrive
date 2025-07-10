#!/usr/bin/env python3
"""
TGDrive Web Service - Runs independently from Bot Service
Handles FastAPI web interface and user interactions
"""

import asyncio
import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

import config
from utils.logger import Logger
from utils.shared_comm import shared_comm

logger = Logger(__name__)

# FastAPI app
app = FastAPI(title="TGDrive Web Service")

# Mount static files and templates (with error handling)
try:
    if Path("static").exists():
        app.mount("/static", StaticFiles(directory="static"), name="static")
    else:
        logger.warning("Static directory not found, creating empty directory")
        Path("static").mkdir(exist_ok=True)
        app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    logger.error(f"Error mounting static files: {e}")

try:
    if Path("templates").exists():
        templates = Jinja2Templates(directory="templates")
    else:
        logger.warning("Templates directory not found, creating empty directory")
        Path("templates").mkdir(exist_ok=True)
        templates = Jinja2Templates(directory="templates")
except Exception as e:
    logger.error(f"Error setting up templates: {e}")
    templates = None

class WebService:
    def __init__(self):
        self.running = False
        
    async def startup(self):
        """Web service startup"""
        logger.info("🌐 Starting TGDrive Web Service...")
        shared_comm.update_web_status("starting", {"message": "Initializing web service"})
        
        # Start background tasks
        asyncio.create_task(self.status_updater())
        asyncio.create_task(self.bot_health_monitor())
        
        self.running = True
        shared_comm.update_web_status("running", {
            "message": "Web service running",
            "port": 8000
        })
        
        logger.info("🎉 Web Service started successfully!")
    
    async def shutdown(self):
        """Web service shutdown"""
        logger.info("🛑 Stopping Web Service...")
        self.running = False
        shared_comm.update_web_status("stopped", {"message": "Web service stopped"})
    
    async def status_updater(self):
        """Regularly update web status"""
        while self.running:
            try:
                shared_comm.update_web_status("running", {
                    "port": 8000,
                    "endpoints_active": True
                })
                await asyncio.sleep(30)  # Update every 30 seconds
            except Exception as e:
                logger.error(f"Status updater error: {e}")
                await asyncio.sleep(60)
    
    async def bot_health_monitor(self):
        """Monitor bot service health"""
        while self.running:
            try:
                health = shared_comm.health_check()
                if not health["bot_healthy"]:
                    logger.warning("⚠️ Bot service appears to be unhealthy")
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Bot health monitor error: {e}")
                await asyncio.sleep(60)

# Global web service instance
web_service = WebService()

# Event handlers
@app.on_event("startup")
async def startup_event():
    await web_service.startup()

@app.on_event("shutdown")
async def shutdown_event():
    await web_service.shutdown()

# API Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main drive interface"""
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse("<h1>TGDrive - Templates not found</h1><p>Please set up templates directory.</p>")

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    """Admin interface"""
    if templates:
        return templates.TemplateResponse("admin.html", {"request": request})
    else:
        return HTMLResponse("<h1>TGDrive Admin - Templates not found</h1><p>Please set up templates directory.</p>")

@app.get("/api/health")
async def health_check():
    """System health check endpoint"""
    health = shared_comm.health_check()
    return {
        "status": "healthy" if health["bot_healthy"] and health["web_healthy"] else "degraded",
        "timestamp": time.time(),
        "services": {
            "bot": "healthy" if health["bot_healthy"] else "unhealthy",
            "web": "healthy" if health["web_healthy"] else "unhealthy"
        },
        "details": health
    }

@app.get("/api/bot/status")
async def bot_status():
    """Get bot service status"""
    if not shared_comm.is_bot_running():
        raise HTTPException(status_code=503, detail="Bot service not running")
    
    status = shared_comm.get_bot_status()
    return status

@app.post("/api/bot/command")
async def send_bot_command(request: Request):
    """Send command to bot service"""
    if not shared_comm.is_bot_running():
        raise HTTPException(status_code=503, detail="Bot service not running")
    
    data = await request.json()
    command = data.get("command")
    params = data.get("params", {})
    
    if not command:
        raise HTTPException(status_code=400, detail="Command is required")
    
    # Send command to bot
    shared_comm.send_command(command, params)
    
    return {"status": "command_sent", "command": command}

@app.get("/api/drive/folders")
async def get_folders():
    """Get all folders for folder picker"""
    # This would normally get data from DRIVE_DATA via bot service
    # For now, return empty structure
    return {"folders": {}}

@app.post("/api/drive/folder")
async def create_folder(request: Request):
    """Create new folder"""
    if not shared_comm.is_bot_running():
        raise HTTPException(status_code=503, detail="Bot service not running")
    
    data = await request.json()
    path = data.get("path", "/")
    name = data.get("name", "New Folder")
    
    # Send command to bot service
    shared_comm.send_command("create_folder", {"path": path, "name": name})
    
    return {"status": "folder_creation_requested"}

@app.post("/api/drive/delete")
async def delete_item(request: Request):
    """Delete file or folder"""
    if not shared_comm.is_bot_running():
        raise HTTPException(status_code=503, detail="Bot service not running")
    
    data = await request.json()
    path = data.get("path")
    
    if not path:
        raise HTTPException(status_code=400, detail="Path is required")
    
    # Send command to bot service
    shared_comm.send_command("delete_item", {"path": path})
    
    return {"status": "deletion_requested"}

@app.post("/api/drive/move")
async def move_items(request: Request):
    """Move files/folders"""
    if not shared_comm.is_bot_running():
        raise HTTPException(status_code=503, detail="Bot service not running")
    
    data = await request.json()
    file_ids = data.get("file_ids", [])
    destination = data.get("destination", "/")
    
    if not file_ids:
        raise HTTPException(status_code=400, detail="File IDs are required")
    
    # Send command to bot service
    shared_comm.send_command("move_items", {"file_ids": file_ids, "destination": destination})
    
    return {"status": "move_requested"}

@app.get("/api/drive/data")
async def get_drive_data():
    """Get current drive data"""
    # Get data from shared communication
    drive_data = shared_comm.get_drive_data()
    last_sync = shared_comm.get_last_sync_time()
    
    return {
        "data": drive_data,
        "last_sync": last_sync,
        "sync_age_seconds": time.time() - last_sync if last_sync else None
    }

@app.post("/api/drive/sync")
async def sync_drive_data():
    """Request drive data sync from bot"""
    if not shared_comm.is_bot_running():
        raise HTTPException(status_code=503, detail="Bot service not running")
    
    # Request sync from bot service
    shared_comm.send_command("sync_drive_data", {})
    
    return {"status": "sync_requested"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )

def run_web_service(host: str = "0.0.0.0", port: int = 8000):
    """Run the web service"""
    logger.info(f"🚀 Starting web service on {host}:{port}")
    uvicorn.run(
        "web_service:app",
        host=host,
        port=port,
        reload=False,  # Disable auto-reload for production
        log_level="info"
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TGDrive Web Service")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", default=8000, type=int, help="Port to bind to")
    args = parser.parse_args()
    
    run_web_service(args.host, args.port)