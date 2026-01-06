"""
ML prediction service for content performance
"""
from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime
import joblib
import os


class PredictionService:
    def __init__(self):
        # Load models if they exist
        self.engagement_model = None
        self.growth_model = None
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained ML models"""
        model_dir = "ml_models/models"
        if os.path.exists(f"{model_dir}/engagement_predictor.pkl"):
            self.engagement_model = joblib.load(f"{model_dir}/engagement_predictor.pkl")
        if os.path.exists(f"{model_dir}/growth_forecaster.pkl"):
            self.growth_model = joblib.load(f"{model_dir}/growth_forecaster.pkl")
    
    def predict_engagement(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict engagement rate for a post"""
        if not self.engagement_model:
            # Return default prediction if model not available
            return {
                "predicted_engagement_rate": Decimal("0.05"),
                "confidence": Decimal("0.5"),
                "recommendation": "Model not trained yet. Post during peak hours (6-9 PM) for best results."
            }
        
        # Extract features
        features = self._extract_features(post_data)
        
        # Predict
        prediction = self.engagement_model.predict([features])[0]
        confidence = float(self.engagement_model.predict_proba([features]).max())
        
        return {
            "predicted_engagement_rate": Decimal(str(prediction)),
            "confidence": Decimal(str(confidence)),
            "recommendation": self._generate_recommendation(prediction, confidence)
        }
    
    def predict_streams_lift(self, post_data: Dict[str, Any]) -> Optional[int]:
        """Predict Spotify streams lift from social content"""
        if not self.growth_model:
            return None
        
        features = self._extract_features(post_data)
        prediction = self.growth_model.predict([features])[0]
        return int(prediction)
    
    def _extract_features(self, post_data: Dict[str, Any]) -> list:
        """Convert post data to model features"""
        scheduled_for = post_data.get("scheduled_for")
        if scheduled_for:
            if isinstance(scheduled_for, str):
                scheduled_for = datetime.fromisoformat(scheduled_for.replace('Z', '+00:00'))
            hour = scheduled_for.hour
            day_of_week = scheduled_for.weekday()
        else:
            hour = datetime.now().hour
            day_of_week = datetime.now().weekday()
        
        caption = post_data.get("caption", "")
        caption_length = len(caption) if caption else 0
        has_hashtags = 1 if "#" in caption else 0
        
        # Content type encoding (simplified)
        content_type_map = {
            "reel": 1,
            "story": 2,
            "tiktok": 3,
            "youtube_short": 4,
            "post": 5
        }
        content_type_encoded = content_type_map.get(post_data.get("content_type", "post"), 5)
        
        return [
            hour,
            day_of_week,
            caption_length,
            has_hashtags,
            content_type_encoded,
        ]
    
    def _generate_recommendation(self, engagement_rate: float, confidence: float) -> str:
        """Generate recommendation based on prediction"""
        if engagement_rate > 0.1:
            return "High engagement predicted! This content should perform well."
        elif engagement_rate > 0.05:
            return "Moderate engagement expected. Consider posting during peak hours."
        else:
            return "Low engagement predicted. Try adjusting caption or posting time."

