"""
FastAPI application entry point for Multi-Artist Music Marketing Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
from backend.config import settings
from backend.database import engine, Base
from backend.routers import auth, connections, callbacks, metrics, content, ai
from backend.jobs import sync_all_artists_data, process_publishing_queue, generate_weekly_insights

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Fanbase Builder - Music Marketing Platform",
    description="Multi-tenant SaaS platform for music artists to manage marketing",
    version="0.1.0"
)

# CORS middleware - support both local dev and production
cors_origins = settings.CORS_ORIGINS.copy()
if settings.FRONTEND_URL:
    cors_origins.append(settings.FRONTEND_URL)
# Also allow Vercel preview URLs
cors_origins.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(connections.router, prefix="/api/connect", tags=["connections"])
app.include_router(callbacks.router, prefix="/api/callback", tags=["callbacks"])
app.include_router(connections.router, prefix="/api/connections", tags=["connections"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

# Initialize scheduler
scheduler = AsyncIOScheduler()

# Schedule background jobs
scheduler.add_job(
    sync_all_artists_data,
    CronTrigger(hour=2, minute=0),  # 2 AM daily
    id="daily_data_sync",
    name="Daily Data Sync",
    replace_existing=True
)

scheduler.add_job(
    process_publishing_queue,
    IntervalTrigger(minutes=5),  # Every 5 minutes
    id="publishing_queue",
    name="Process Publishing Queue",
    replace_existing=True
)

scheduler.add_job(
    generate_weekly_insights,
    CronTrigger(day_of_week="mon", hour=8),  # Monday at 8 AM
    id="weekly_insights",
    name="Generate Weekly Insights",
    replace_existing=True
)

# Start scheduler
scheduler.start()
logger.info("Background scheduler started")

@app.get("/")
async def root():
    return {
        "message": "Fanbase Builder API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Test database connection
        from backend.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown scheduler on app shutdown"""
    scheduler.shutdown()
    logger.info("Background scheduler stopped")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

