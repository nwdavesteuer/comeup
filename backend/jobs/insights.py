"""
Weekly insights generation job
"""
import logging
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.artist import Artist
from backend.services.insights_service import InsightsService

logger = logging.getLogger(__name__)
insights_service = InsightsService()


async def generate_weekly_insights():
    """
    Generate weekly insights for all artists.
    Runs every Monday at 8 AM.
    """
    db: Session = SessionLocal()
    try:
        artists = db.query(Artist).all()
        
        logger.info(f"Generating weekly insights for {len(artists)} artists")
        
        for artist in artists:
            try:
                insights = await insights_service.generate_weekly_insights(db, str(artist.artist_id))
                logger.info(f"Generated insights for artist {artist.artist_id}")
                # In production, would email insights or store in database
            except Exception as e:
                logger.error(f"Error generating insights for artist {artist.artist_id}: {str(e)}")
                continue
        
        logger.info("Weekly insights generation completed")
    finally:
        db.close()

