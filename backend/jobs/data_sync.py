"""
Daily data sync job - syncs metrics from all platforms
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.artist import Artist
from backend.models.connection import PlatformConnection
from backend.models.metric import DailyMetric
from backend.utils.encryption import decrypt_token
from backend.services.spotify_service import SpotifyService
from backend.services.instagram_service import InstagramService
from backend.services.tiktok_service import TikTokService
from backend.services.youtube_service import YouTubeService

logger = logging.getLogger(__name__)


async def sync_all_artists_data():
    """
    Daily job to sync data from all connected platforms.
    Runs at 2 AM daily.
    """
    db: Session = SessionLocal()
    try:
        # Get all artists with active connections
        artists = db.query(Artist).join(PlatformConnection).filter(
            PlatformConnection.is_active == True
        ).all()
        
        logger.info(f"Starting data sync for {len(artists)} artists")
        
        for artist in artists:
            try:
                await sync_artist_data(db, artist)
            except Exception as e:
                logger.error(f"Error syncing data for artist {artist.artist_id}: {str(e)}")
                continue
        
        logger.info("Data sync completed")
    finally:
        db.close()


async def sync_artist_data(db: Session, artist: Artist):
    """Sync data for a single artist"""
    connections = db.query(PlatformConnection).filter(
        PlatformConnection.artist_id == artist.artist_id,
        PlatformConnection.is_active == True
    ).all()
    
    for connection in connections:
        try:
            # Refresh token if needed
            if connection.token_expires_at and connection.token_expires_at < datetime.utcnow():
                await refresh_token(db, connection)
            
            # Sync platform data
            if connection.platform == "spotify":
                await sync_spotify_data(db, artist, connection)
            elif connection.platform == "instagram":
                await sync_instagram_data(db, artist, connection)
            elif connection.platform == "tiktok":
                await sync_tiktok_data(db, artist, connection)
            elif connection.platform == "youtube":
                await sync_youtube_data(db, artist, connection)
            
            # Update last_sync
            connection.last_sync = datetime.utcnow()
            db.commit()
            
        except Exception as e:
            logger.error(f"Error syncing {connection.platform} for artist {artist.artist_id}: {str(e)}")
            continue


async def refresh_token(db: Session, connection: PlatformConnection):
    """Refresh OAuth token if expired"""
    if not connection.refresh_token:
        logger.warning(f"No refresh token for {connection.platform} connection {connection.connection_id}")
        return
    
    try:
        decrypted_refresh = decrypt_token(connection.refresh_token)
        
        if connection.platform == "spotify":
            tokens = await SpotifyService.refresh_token(decrypted_refresh)
        elif connection.platform == "tiktok":
            tokens = await TikTokService.refresh_token(decrypted_refresh)
        elif connection.platform == "youtube":
            tokens = await YouTubeService.refresh_token(decrypted_refresh)
        else:
            logger.warning(f"Token refresh not implemented for {connection.platform}")
            return
        
        # Update tokens
        from backend.utils.encryption import encrypt_token
        connection.access_token = encrypt_token(tokens["access_token"])
        if "refresh_token" in tokens:
            connection.refresh_token = encrypt_token(tokens["refresh_token"])
        connection.token_expires_at = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
        db.commit()
        
    except Exception as e:
        logger.error(f"Error refreshing token for {connection.platform}: {str(e)}")


async def sync_spotify_data(db: Session, artist: Artist, connection: PlatformConnection):
    """Sync Spotify data"""
    from backend.utils.encryption import decrypt_token
    
    access_token = decrypt_token(connection.access_token)
    stats = await SpotifyService.get_artist_stats(access_token)
    
    # Store metrics (simplified - would need actual Spotify API endpoints)
    today = datetime.utcnow().date()
    
    # Example: store monthly listeners if available
    # This would need actual Spotify for Artists API integration
    metric = DailyMetric(
        artist_id=artist.artist_id,
        date=today,
        platform="spotify",
        metric_name="monthly_listeners",
        value=0  # Placeholder
    )
    
    # Check if metric already exists
    existing = db.query(DailyMetric).filter(
        DailyMetric.artist_id == artist.artist_id,
        DailyMetric.date == today,
        DailyMetric.platform == "spotify",
        DailyMetric.metric_name == "monthly_listeners"
    ).first()
    
    if not existing:
        db.add(metric)
        db.commit()


async def sync_instagram_data(db: Session, artist: Artist, connection: PlatformConnection):
    """Sync Instagram data"""
    from backend.utils.encryption import decrypt_token
    
    access_token = decrypt_token(connection.access_token)
    insights = await InstagramService.get_user_insights(access_token)
    
    today = datetime.utcnow().date()
    
    # Store follower count if available
    if "followers_count" in insights:
        metric = DailyMetric(
            artist_id=artist.artist_id,
            date=today,
            platform="instagram",
            metric_name="followers",
            value=insights.get("followers_count", 0)
        )
        
        existing = db.query(DailyMetric).filter(
            DailyMetric.artist_id == artist.artist_id,
            DailyMetric.date == today,
            DailyMetric.platform == "instagram",
            DailyMetric.metric_name == "followers"
        ).first()
        
        if not existing:
            db.add(metric)
            db.commit()


async def sync_tiktok_data(db: Session, artist: Artist, connection: PlatformConnection):
    """Sync TikTok data"""
    from backend.utils.encryption import decrypt_token
    
    access_token = decrypt_token(connection.access_token)
    stats = await TikTokService.get_user_stats(access_token)
    
    today = datetime.utcnow().date()
    
    # Store follower count if available
    if "follower_count" in stats:
        metric = DailyMetric(
            artist_id=artist.artist_id,
            date=today,
            platform="tiktok",
            metric_name="followers",
            value=stats.get("follower_count", 0)
        )
        
        existing = db.query(DailyMetric).filter(
            DailyMetric.artist_id == artist.artist_id,
            DailyMetric.date == today,
            DailyMetric.platform == "tiktok",
            DailyMetric.metric_name == "followers"
        ).first()
        
        if not existing:
            db.add(metric)
            db.commit()


async def sync_youtube_data(db: Session, artist: Artist, connection: PlatformConnection):
    """Sync YouTube data"""
    from backend.utils.encryption import decrypt_token
    
    access_token = decrypt_token(connection.access_token)
    stats = await YouTubeService.get_channel_stats(access_token)
    
    today = datetime.utcnow().date()
    
    # Store subscriber count if available
    if "items" in stats and len(stats["items"]) > 0:
        channel = stats["items"][0]
        if "statistics" in channel:
            subscribers = channel["statistics"].get("subscriberCount", 0)
            
            metric = DailyMetric(
                artist_id=artist.artist_id,
                date=today,
                platform="youtube",
                metric_name="subscribers",
                value=int(subscribers) if subscribers else 0
            )
            
            existing = db.query(DailyMetric).filter(
                DailyMetric.artist_id == artist.artist_id,
                DailyMetric.date == today,
                DailyMetric.platform == "youtube",
                DailyMetric.metric_name == "subscribers"
            ).first()
            
            if not existing:
                db.add(metric)
                db.commit()

