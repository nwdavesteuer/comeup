"""
FastAPI application entry point for Multi-Artist Music Marketing Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Fanbase Builder - Music Marketing Platform",
    description="Multi-tenant SaaS platform for music artists to manage marketing",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Fanbase Builder API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routers (will be created next)
# from backend.routers import auth, artists, connections

# app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
# app.include_router(artists.router, prefix="/api/artists", tags=["artists"])
# app.include_router(connections.router, prefix="/api/connections", tags=["connections"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

