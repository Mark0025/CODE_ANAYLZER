from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func
from loguru import logger
from code_analyzer.models import LogEntry, get_session
import os
import asyncio
from fastapi import WebSocketDisconnect

app = FastAPI()

# Setup templates and static files
templates = Jinja2Templates(directory="code_analyzer/monitoring/templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
@app.get("/dashboard")
async def dashboard(request: Request):
    """Main dashboard view."""
    session = get_session()
    try:
        # Get recent logs
        logs = session.query(LogEntry)\
            .order_by(LogEntry.timestamp.desc())\
            .limit(10)\
            .all()
            
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "logs": logs,
                "active_crews": ["DEV-NOW", "ANALYZER"],
                "recent_operations": ["Analysis", "Fix", "Test"],
                "system_health": "OK"
            }
        )
    finally:
        session.close()

@app.get("/crews")
async def crews(request: Request):
    """Crews view."""
    return templates.TemplateResponse(
        "crews.html",
        {
            "request": request,
            "crews": ["DEV-NOW", "ANALYZER"]
        }
    )

@app.get("/analysis")
async def analysis(request: Request):
    """Analysis view."""
    return templates.TemplateResponse(
        "analysis.html",
        {
            "request": request
        }
    )

@app.get("/api/logs")
async def get_logs():
    """Get recent logs."""
    session = get_session()
    try:
        logs = session.query(LogEntry)\
            .order_by(LogEntry.timestamp.desc())\
            .limit(10)\
            .all()
        return {"logs": [log.to_dict() for log in logs]}
    finally:
        session.close()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    try:
        while True:
            session = get_session()
            try:
                logs = session.query(LogEntry)\
                    .order_by(LogEntry.timestamp.desc())\
                    .limit(5)\
                    .all()
                
                await websocket.send_json({
                    "type": "logs",
                    "data": [log.to_dict() for log in logs]
                })
            finally:
                session.close()
            
            await asyncio.sleep(1)  # Add delay to prevent rapid updates
            
    except WebSocketDisconnect:
        pass  # Client disconnected
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

@app.get("/DEV-NOW")
async def dev_now(request: Request):
    """DEV-NOW view."""
    session = get_session()
    try:
        # Get recent logs
        logs = session.query(LogEntry)\
            .order_by(LogEntry.timestamp.desc())\
            .limit(10)\
            .all()
            
        return templates.TemplateResponse(
            "dev_now.html",
            {
                "request": request,
                "logs": logs,
                "active_crews": ["DEV-NOW", "ANALYZER"],
                "recent_operations": ["Analysis", "Fix", "Test"],
                "system_health": "OK"
            }
        )
    finally:
        session.close()

@app.get("/timeline")
async def timeline(request: Request):
    """Timeline view."""
    session = get_session()
    try:
        events = session.query(LogEntry)\
            .order_by(LogEntry.timestamp.desc())\
            .limit(20)\
            .all()
            
        return templates.TemplateResponse(
            "timeline.html",
            {
                "request": request,
                "events": events
            }
        )
    finally:
        session.close()

@app.get("/analytics")
async def analytics(request: Request):
    """Analytics view."""
    session = get_session()
    try:
        # Get analytics data
        total_logs = session.query(func.count(LogEntry.id)).scalar()
        level_counts = session.query(
            LogEntry.level, 
            func.count(LogEntry.id).label('count')
        ).group_by(LogEntry.level).all()
        
        crew_stats = session.query(
            LogEntry.crew_name,
            func.count(LogEntry.id).label('total_ops')
        ).group_by(LogEntry.crew_name).all()
        
        return templates.TemplateResponse(
            "analytics.html",
            {
                "request": request,
                "total_logs": total_logs,
                "level_counts": dict(level_counts),
                "crew_stats": crew_stats
            }
        )
    finally:
        session.close() 