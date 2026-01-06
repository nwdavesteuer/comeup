"""
Publishing queue job - publishes scheduled content
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.content import ContentPost

logger = logging.getLogger(__name__)


async def process_publishing_queue():
    """
    Process scheduled posts that are ready to publish.
    Runs every 5 minutes.
    """
    db: Session = SessionLocal()
    try:
        # Find posts scheduled for the next 5 minutes
        now = datetime.utcnow()
        cutoff = now + timedelta(minutes=5)
        
        posts = db.query(ContentPost).filter(
            ContentPost.status == "scheduled",
            ContentPost.scheduled_for <= cutoff,
            ContentPost.scheduled_for >= now
        ).all()
        
        logger.info(f"Processing {len(posts)} scheduled posts")
        
        for post in posts:
            try:
                await publish_post(db, post)
            except Exception as e:
                logger.error(f"Error publishing post {post.post_id}: {str(e)}")
                post.status = "failed"
                db.commit()
        
    finally:
        db.close()


async def publish_post(db: Session, post: ContentPost):
    """Publish a post to its platform"""
    # This is a placeholder - actual implementation would:
    # 1. Get platform connection
    # 2. Call platform API to create post
    # 3. Update post with external_url
    # 4. Mark as published
    
    logger.info(f"Publishing {post.content_type} to {post.platform} for post {post.post_id}")
    
    # Placeholder: mark as published
    post.status = "published"
    post.posted_at = datetime.utcnow()
    post.external_url = f"https://{post.platform}.com/post/{post.post_id}"  # Placeholder
    
    db.commit()
    
    logger.info(f"Post {post.post_id} published successfully")

