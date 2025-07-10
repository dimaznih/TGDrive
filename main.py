#!/usr/bin/env python3
"""
TGDrive Main Entry Point - Web Service Only
Bot service runs separately via bot_service.py
"""

from web_service import app

# Import the FastAPI app from web_service
# This allows uvicorn to run: uvicorn main:app --host 0.0.0.0 --port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=False  # Disable reload for production
    )
