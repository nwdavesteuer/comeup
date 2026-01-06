"""
Content schedule generation service
Creates personalized content schedules based on onboarding data
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta
from backend.models.onboarding import OnboardingResponse


class ContentScheduleService:
    """Generate content schedules based on artist persona"""
    
    @staticmethod
    def generate_weekly_schedule(onboarding: OnboardingResponse) -> List[Dict[str, Any]]:
        """
        Generate a week's content schedule based on onboarding responses
        
        Returns a list of content suggestions with:
        - day (Monday, Tuesday, etc.)
        - platform (instagram, tiktok)
        - content_type (reel, post, story, etc.)
        - idea (description of what to post)
        - time_suggestion (best time to post)
        """
        schedule = []
        
        # Determine posting frequency based on available time
        hours = onboarding.content_hours_per_week
        if hours == 'less_than_2':
            posts_per_week = 2
        elif hours == '2_5':
            posts_per_week = 3
        elif hours == '5_10':
            posts_per_week = 5
        elif hours == '10_15':
            posts_per_week = 7
        else:  # more_than_15
            posts_per_week = 10
        
        # Get preferred content types
        content_types = onboarding.preferred_content_types or []
        if 'all' in content_types or not content_types:
            # Default to high-performing types
            content_types = ['behind_scenes', 'music_snippets', 'trends']
        
        # Determine platforms (focus on Instagram and TikTok for MVP)
        platforms = ['instagram', 'tiktok']
        
        # Generate schedule for next 7 days
        today = datetime.now().date()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Distribute posts across the week
        posts_created = 0
        for i in range(7):
            day_date = today + timedelta(days=i)
            day_name = days_of_week[day_date.weekday()]
            
            # Determine how many posts for this day
            posts_today = 0
            if posts_created < posts_per_week:
                # Distribute evenly, with more on weekdays
                if day_date.weekday() < 5:  # Weekday
                    if posts_created < posts_per_week - 2:
                        posts_today = 1
                else:  # Weekend
                    if posts_created < posts_per_week and posts_per_week > 5:
                        posts_today = 1
            
            # Generate posts for this day
            for j in range(posts_today):
                platform = platforms[posts_created % len(platforms)]
                content_type = content_types[posts_created % len(content_types)]
                
                # Generate content idea based on type
                idea = ContentScheduleService._generate_content_idea(
                    content_type, onboarding, day_name
                )
                
                schedule.append({
                    'day': day_name,
                    'date': day_date.isoformat(),
                    'platform': platform,
                    'content_type': content_type,
                    'idea': idea,
                    'time_suggestion': ContentScheduleService._get_best_time(platform),
                    'estimated_time': ContentScheduleService._estimate_time(content_type)
                })
                
                posts_created += 1
                if posts_created >= posts_per_week:
                    break
            
            if posts_created >= posts_per_week:
                break
        
        return schedule
    
    @staticmethod
    def _generate_content_idea(content_type: str, onboarding: OnboardingResponse, day: str) -> str:
        """Generate a specific content idea based on type and onboarding data"""
        ideas = {
            'behind_scenes': [
                "Share a clip from your recording session",
                "Show your songwriting process",
                "Behind-the-scenes of creating your latest track",
                "A day in the studio",
            ],
            'music_snippets': [
                "Preview of your new song",
                "Hook from your latest track",
                "30-second snippet of your best verse",
                "Chorus preview",
            ],
            'performance': [
                "Acoustic version of your song",
                "Live performance clip",
                "Cover of a song that inspired you",
            ],
            'trends': [
                "Jump on the latest audio trend",
                "Participate in a viral challenge",
                "Trending sound with your music",
            ],
            'storytelling': [
                "The story behind your latest song",
                "What inspired this track",
                "Your journey as an artist",
            ],
        }
        
        # Use upcoming content if provided
        if onboarding.upcoming_content:
            return f"{onboarding.upcoming_content} - Create content around this"
        
        # Use upcoming music info
        if onboarding.upcoming_music in ['soon', 'unreleased']:
            if content_type == 'music_snippets':
                return "Teaser for your upcoming release"
            elif content_type == 'behind_scenes':
                return "Behind-the-scenes of creating your upcoming release"
        
        # Default ideas
        type_ideas = ideas.get(content_type, ["Create engaging content for your audience"])
        return type_ideas[hash(day) % len(type_ideas)]
    
    @staticmethod
    def _get_best_time(platform: str) -> str:
        """Get best posting time for platform"""
        if platform == 'instagram':
            return "2:00 PM - 3:00 PM"  # Peak engagement time
        elif platform == 'tiktok':
            return "6:00 PM - 10:00 PM"  # Evening peak
        return "12:00 PM - 2:00 PM"
    
    @staticmethod
    def _estimate_time(content_type: str) -> str:
        """Estimate time needed to create content"""
        estimates = {
            'behind_scenes': '15-30 min',
            'music_snippets': '10-20 min',
            'performance': '20-40 min',
            'trends': '15-25 min',
            'storytelling': '20-30 min',
        }
        return estimates.get(content_type, '20-30 min')
    
    @staticmethod
    def generate_schedule_summary(schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of the schedule"""
        total_posts = len(schedule)
        platforms = {}
        content_types = {}
        
        for item in schedule:
            platform = item['platform']
            content_type = item['content_type']
            platforms[platform] = platforms.get(platform, 0) + 1
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        return {
            'total_posts': total_posts,
            'posts_by_platform': platforms,
            'posts_by_type': content_types,
            'estimated_total_time': f"{total_posts * 20}-{total_posts * 30} minutes"
        }

