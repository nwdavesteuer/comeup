"""
AI insights generation service using Claude API
"""
import anthropic
from typing import Dict, Any, List
from backend.config import settings
from sqlalchemy.orm import Session
from backend.models.metric import DailyMetric
from backend.models.content import ContentPost
from datetime import datetime, timedelta


class InsightsService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None
    
    async def generate_weekly_insights(self, db: Session, artist_id: str) -> str:
        """Generate weekly strategic insights using Claude API"""
        if not self.client:
            return "AI insights unavailable - API key not configured"
        
        # Gather last week's data
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        metrics = db.query(DailyMetric).filter(
            DailyMetric.artist_id == artist_id,
            DailyMetric.date >= week_ago.date()
        ).all()
        
        content = db.query(ContentPost).filter(
            ContentPost.artist_id == artist_id,
            ContentPost.created_at >= week_ago
        ).all()
        
        # Build prompt
        prompt = self._build_insights_prompt(metrics, content)
        
        # Call Claude API
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def _build_insights_prompt(self, metrics: List[DailyMetric], content: List[ContentPost]) -> str:
        """Build prompt for Claude API"""
        metrics_summary = {}
        for metric in metrics:
            key = f"{metric.platform}_{metric.metric_name}"
            if key not in metrics_summary:
                metrics_summary[key] = []
            metrics_summary[key].append(metric.value)
        
        prompt = f"""
        Analyze this music artist's weekly performance:
        
        Metrics:
        {self._format_metrics(metrics_summary)}
        
        Content posted: {len(content)} posts
        
        Provide:
        1. Three key insights about what's working
        2. Two specific action items for this week
        3. One experiment to test
        
        Be concise, actionable, and specific to this artist's data.
        """
        return prompt
    
    def _format_metrics(self, metrics_summary: Dict[str, List]) -> str:
        """Format metrics for prompt"""
        formatted = []
        for key, values in metrics_summary.items():
            if values:
                avg = sum(v for v in values if v) / len(values) if values else 0
                formatted.append(f"- {key}: {avg:.0f} (avg)")
        return "\n".join(formatted)

