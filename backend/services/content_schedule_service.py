"""
Content schedule generation service
Creates personalized content schedules based on onboarding data
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from backend.models.onboarding import OnboardingResponse
import random


class ContentScheduleService:
    """Generate content schedules based on artist persona"""
    
    @staticmethod
    def generate_weekly_schedule(onboarding: OnboardingResponse) -> List[Dict[str, Any]]:
        """
        Generate a week's content schedule based on onboarding responses
        
        Returns a list of content items with detailed information including:
        - content_name (unique descriptive name)
        - date (actual date)
        - activity_type (filming, editing, posting)
        - platform
        - format (reel, post, story, tiktok_video, carousel)
        - visual_direction (color palette, style)
        - content_description
        - shot_list (with time ranges)
        - setup_time
        - filming_duration / editing_duration
        - posting_time (if activity_type is posting)
        - caption
        - hashtags
        """
        schedule = []
        
        # Get release date for planning
        release_date = onboarding.specific_release_date
        today = datetime.now().date()
        
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
        
        # Get preferred content types (prioritize what's working)
        content_types = onboarding.preferred_content_types or []
        whats_working = onboarding.whats_working or []
        
        # Prioritize content types that are working
        if whats_working:
            # Filter to only include types that are working
            working_types = [ct for ct in content_types if ct in whats_working]
            if working_types:
                content_types = working_types
        
        if 'all' in content_types or not content_types:
            # Default to high-performing types
            content_types = ['behind_scenes', 'music_snippets', 'trends']
        
        # Determine platforms based on content type
        platforms = ['instagram', 'tiktok']
        
        # Generate content for the week
        # Plan filming and editing days, then group posting days at the end
        content_items = []
        
        for i in range(posts_per_week):
            # Determine content type and platform
            content_type = content_types[i % len(content_types)]
            platform = platforms[i % len(platforms)]
            
            # Generate unique content name
            content_name = ContentScheduleService._generate_content_name(
                content_type, platform, i, onboarding
            )
            
            # Determine dates: filming 2-3 days before editing, editing 1 day before posting
            # Posting days will be grouped at the end
            base_date = today + timedelta(days=i*2)  # Spread out filming days
            filming_date = base_date
            editing_date = base_date + timedelta(days=2)
            posting_date = base_date + timedelta(days=3)
            
            # Generate detailed content information
            content_info = ContentScheduleService._generate_detailed_content(
                content_name, content_type, platform, onboarding, posting_date, release_date
            )
            
            # Add filming day
            content_items.append({
                'content_name': content_name,
                'date': filming_date.isoformat(),
                'activity_type': 'filming',
                'platform': platform,
                'format': content_info['format'],
                'visual_direction': content_info['visual_direction'],
                'content_description': content_info['content_description'],
                'shot_list': content_info['shot_list'],
                'setup_time': content_info['setup_time'],
                'filming_duration': content_info['filming_duration'],
            })
            
            # Add editing day
            content_items.append({
                'content_name': content_name,
                'date': editing_date.isoformat(),
                'activity_type': 'editing',
                'platform': platform,
                'format': content_info['format'],
                'editing_duration': content_info['editing_duration'],
            })
            
            # Add posting day (will be sorted to end)
            content_items.append({
                'content_name': content_name,
                'date': posting_date.isoformat(),
                'activity_type': 'posting',
                'platform': platform,
                'format': content_info['format'],
                'posting_time': content_info['posting_time'],
                'caption': content_info['caption'],
                'hashtags': content_info['hashtags'],
            })
        
        # Sort: filming and editing first (chronologically), then posting days at the end
        filming_editing = [item for item in content_items if item['activity_type'] in ['filming', 'editing']]
        posting = [item for item in content_items if item['activity_type'] == 'posting']
        
        # Sort each group by date
        filming_editing.sort(key=lambda x: x['date'])
        posting.sort(key=lambda x: x['date'])
        
        # Combine: filming/editing first, then posting
        schedule = filming_editing + posting
        
        return schedule
    
    @staticmethod
    def _generate_content_name(content_type: str, platform: str, index: int, onboarding: OnboardingResponse) -> str:
        """Generate a unique descriptive name for content"""
        visual_styles = onboarding.visual_styles or []
        style_name = visual_styles[0] if visual_styles else "authentic"
        
        # Map style names to readable format
        style_map = {
            'natural': 'Natural',
            'vintage': 'Vintage',
            'moody': 'Moody',
            'minimalist': 'Minimalist',
            'urban': 'Urban',
            'studio': 'Studio'
        }
        style_display = style_map.get(style_name, 'Authentic')
        
        # Map content types to readable format
        type_map = {
            'behind_scenes': 'Behind-the-Scenes',
            'music_snippets': 'Music Snippet',
            'performance': 'Performance',
            'trends': 'Trend',
            'storytelling': 'Storytelling',
            'lifestyle': 'Lifestyle',
            'educational': 'Educational'
        }
        type_display = type_map.get(content_type, 'Content')
        
        # Map platforms
        platform_map = {
            'instagram': 'Instagram',
            'tiktok': 'TikTok'
        }
        platform_display = platform_map.get(platform, 'Social')
        
        # Generate unique name - include song name if available
        song_name = onboarding.song_name or ""
        if onboarding.specific_release_date:
            days_until_release = (onboarding.specific_release_date.date() - datetime.now().date()).days
            if 0 <= days_until_release <= 14:
                if song_name:
                    return f"{style_display} {type_display} - {song_name} (Pre-Release)"
                return f"{style_display} {type_display} - Pre-Release Content"
        
        if song_name:
            return f"{style_display} {type_display} - {song_name}"
        
        return f"{style_display} {type_display} - {platform_display} {index + 1}"
    
    @staticmethod
    def _generate_detailed_content(
        content_name: str, 
        content_type: str, 
        platform: str, 
        onboarding: OnboardingResponse,
        posting_date: datetime.date,
        release_date: Optional[datetime]
    ) -> Dict[str, Any]:
        """Generate detailed content information"""
        
        # Get visual style for color palette and direction
        visual_styles = onboarding.visual_styles or ['natural']
        visual_style = visual_styles[0]
        
        # Get genre/inspiration for content ideas
        inspiring_artists = onboarding.inspiring_artists or ""
        genre = onboarding.genre_fallback or ""
        
        # Determine format based on platform and content type
        if platform == 'instagram':
            if content_type == 'music_snippets':
                format_type = 'reel'
            elif content_type == 'behind_scenes':
                format_type = 'reel'
            elif content_type == 'storytelling':
                format_type = 'carousel'
            else:
                format_type = 'post'
        else:  # tiktok
            format_type = 'tiktok_video'
        
        # Generate visual direction based on style
        visual_direction = ContentScheduleService._get_visual_direction(visual_style)
        
        # Generate content description
        song_name = onboarding.song_name or ""
        content_description = ContentScheduleService._get_content_description(
            content_type, visual_style, inspiring_artists, genre, onboarding, song_name
        )
        
        # Generate shot list
        shot_list = ContentScheduleService._get_shot_list(content_type, visual_style)
        
        # Get time estimates
        setup_time = ContentScheduleService._get_setup_time(content_type)
        filming_duration = ContentScheduleService._get_filming_duration(content_type)
        editing_duration = ContentScheduleService._get_editing_duration(format_type)
        
        # Get posting time
        posting_time = ContentScheduleService._get_posting_time(platform)
        
        # Generate caption and hashtags
        song_name = onboarding.song_name or ""
        caption = ContentScheduleService._generate_caption(
            content_type, onboarding, release_date, posting_date, song_name
        )
        hashtags = ContentScheduleService._generate_hashtags(content_type, genre, inspiring_artists)
        
        return {
            'format': format_type,
            'visual_direction': visual_direction,
            'content_description': content_description,
            'shot_list': shot_list,
            'setup_time': setup_time,
            'filming_duration': filming_duration,
            'editing_duration': editing_duration,
            'posting_time': posting_time,
            'caption': caption,
            'hashtags': hashtags
        }
    
    @staticmethod
    def _get_visual_direction(visual_style: str) -> Dict[str, Any]:
        """Get visual direction including color palette"""
        directions = {
            'natural': {
                'color_palette': 'Warm sepia tones, golden hour palette (oranges #FF8C42, soft yellows #FFD93D, warm whites #FFF8E7)',
                'style_description': 'Natural lighting, unpolished, authentic. Think Clairo\'s "Sofia" music video aesthetic - soft focus, nostalgic, warm tones.'
            },
            'vintage': {
                'color_palette': 'Vintage film aesthetic (warm sepia #D4A574, soft blues #A8C5D1, natural greens #8FA68E)',
                'style_description': 'Film grain overlay, nostalgic feel, warm tones. Reference Boygenius\' album cover style - earthy tones, natural textures.'
            },
            'moody': {
                'color_palette': 'Moody atmospheric tones (deep blues #2C3E50, purples #6C5CE7, dark grays #34495E)',
                'style_description': 'Low light, shadows, dramatic lighting. Similar to The 1975\'s aesthetic - atmospheric, emotional, cinematic.'
            },
            'minimalist': {
                'color_palette': 'Clean minimal palette (whites #FFFFFF, soft grays #E8E8E8, neutral beiges #F5F5DC)',
                'style_description': 'Simple compositions, clean backgrounds, focus on subject. Minimalist aesthetic - less is more.'
            },
            'urban': {
                'color_palette': 'Urban street palette (concrete grays #95A5A6, neon accents #00D2FF, deep blacks #1C1C1C)',
                'style_description': 'Cityscapes, street aesthetic, high contrast. Think JID\'s "Surround Sound" video - dynamic, urban, cinematic.'
            },
            'studio': {
                'color_palette': 'Cozy warm tones (soft oranges #FFB88C, warm whites #FFF5E6, muted greens #A8D5BA)',
                'style_description': 'Intimate indoor setting, warm lighting, cozy atmosphere. Similar to Phoebe Bridgers\' intimate performance videos.'
            }
        }
        return directions.get(visual_style, directions['natural'])
    
    @staticmethod
    def _get_content_description(
        content_type: str, 
        visual_style: str, 
        inspiring_artists: str, 
        genre: str,
        onboarding: OnboardingResponse,
        song_name: str = ""
    ) -> str:
        """Generate detailed content description"""
        base_descriptions = {
            'behind_scenes': 'Show your creative process - recording, writing, or producing. Authentic, unpolished moments that give fans insight into your artistry.',
            'music_snippets': '30-second snippet of your music. Focus on the hook or most engaging part. Make it shareable and memorable.',
            'performance': 'Acoustic or live performance of your song. Intimate setting, focus on the music and emotion.',
            'trends': 'Jump on a trending audio or challenge. Put your unique spin on it while staying true to your style.',
            'storytelling': 'Tell the story behind your music. What inspired it? What does it mean to you? Connect with your audience on a deeper level.',
            'lifestyle': 'Day-in-the-life content. Show your personality, your process, your world. Make it personal and relatable.',
            'educational': 'Share tips, insights, or behind-the-scenes of your craft. Help your audience learn while showcasing your expertise.'
        }
        
        description = base_descriptions.get(content_type, 'Create engaging content for your audience.')
        
        # Add genre/inspiration context if available
        if inspiring_artists:
            description += f' Inspired by {inspiring_artists.split(",")[0].strip() if "," in inspiring_artists else inspiring_artists}.'
        elif genre:
            description += f' {genre} vibes.'
        
        # Add release context if applicable
        if onboarding.specific_release_date:
            days_until = (onboarding.specific_release_date.date() - datetime.now().date()).days
            if 0 <= days_until <= 14:
                if song_name:
                    description += f' Build anticipation for "{song_name}" releasing in {days_until} days.'
                else:
                    description += ' Build anticipation for your upcoming release.'
        
        return description
    
    @staticmethod
    def _get_shot_list(content_type: str, visual_style: str) -> List[Dict[str, str]]:
        """Generate shot list with time ranges"""
        shot_lists = {
            'behind_scenes': [
                {'shot': 'Wide establishing shot', 'time_range': '8-12 min', 'description': 'Walk into frame, find natural spot, set up. Camera at eye level, captures full environment.'},
                {'shot': 'Medium shot of process', 'time_range': '10-15 min', 'description': 'Focus on hands and instrument/equipment, capture 2-3 full takes. Camera at chest level, slight upward angle for warmth.'},
                {'shot': 'Close-up emotional moments', 'time_range': '8-12 min', 'description': 'Capture facial expressions during key moments. Camera at eye level, tight frame.'},
                {'shot': 'B-roll elements', 'time_range': '5-8 min', 'description': 'Natural surroundings, textures, environmental details. Various angles for visual interest.'}
            ],
            'music_snippets': [
                {'shot': 'Main performance shot', 'time_range': '10-15 min', 'description': '3-4 takes of full snippet, different energy levels. Medium-close shot, eye-level camera, slight upward angle for intimacy.'},
                {'shot': 'Close-up hand shots', 'time_range': '5-8 min', 'description': 'Capture fingerpicking, string details, instrument details. Overhead and side angles.'},
                {'shot': 'B-roll ambiance', 'time_range': '5-7 min', 'description': 'Soft focus on environment, lighting, cozy details. Various angles for texture.'}
            ],
            'performance': [
                {'shot': 'Wide performance shot', 'time_range': '10-15 min', 'description': 'Full body or medium-wide, capture performance energy. Eye-level or slight low angle for presence.'},
                {'shot': 'Close-up emotional moments', 'time_range': '8-12 min', 'description': 'Facial expressions, connection with music. Tight frame, eye-level.'},
                {'shot': 'Instrument detail shots', 'time_range': '5-8 min', 'description': 'Hands on instrument, playing techniques. Various close-up angles.'}
            ],
            'trends': [
                {'shot': 'Main trend shot', 'time_range': '8-12 min', 'description': 'Capture the trend/challenge, multiple takes. Medium shot, eye-level, dynamic.'},
                {'shot': 'B-roll for transitions', 'time_range': '5-8 min', 'description': 'Quick cuts, movement, energy. Various angles for editing flexibility.'}
            ],
            'storytelling': [
                {'shot': 'Establishing shot', 'time_range': '8-12 min', 'description': 'Set the scene, environment, context. Wide or medium-wide, eye-level.'},
                {'shot': 'Personal moments', 'time_range': '10-15 min', 'description': 'You telling the story, authentic expressions. Medium-close, eye-level, intimate.'},
                {'shot': 'Detail shots', 'time_range': '5-8 min', 'description': 'Relevant objects, textures, visual metaphors. Various close-up angles.'}
            ]
        }
        
        return shot_lists.get(content_type, shot_lists['behind_scenes'])
    
    @staticmethod
    def _get_setup_time(content_type: str) -> str:
        """Get setup time range"""
        setup_times = {
            'behind_scenes': '10-15 min',
            'music_snippets': '8-12 min',
            'performance': '10-15 min',
            'trends': '5-10 min',
            'storytelling': '10-15 min',
            'lifestyle': '8-12 min',
            'educational': '10-15 min'
        }
        return setup_times.get(content_type, '10-15 min')
    
    @staticmethod
    def _get_filming_duration(content_type: str) -> str:
        """Get filming duration range"""
        durations = {
            'behind_scenes': '30-45 min',
            'music_snippets': '20-30 min',
            'performance': '25-40 min',
            'trends': '15-25 min',
            'storytelling': '30-45 min',
            'lifestyle': '25-35 min',
            'educational': '30-45 min'
        }
        return durations.get(content_type, '25-35 min')
    
    @staticmethod
    def _get_editing_duration(format_type: str) -> str:
        """Get editing duration range"""
        durations = {
            'reel': '20-30 min',
            'post': '15-25 min',
            'carousel': '30-40 min',
            'tiktok_video': '15-20 min',
            'story': '10-15 min'
        }
        return durations.get(format_type, '20-30 min')
    
    @staticmethod
    def _get_posting_time(platform: str) -> str:
        """Get best posting time"""
        if platform == 'instagram':
            return "2:00 PM - 3:00 PM"
        elif platform == 'tiktok':
            return "7:00 PM - 9:00 PM"
        return "2:00 PM - 3:00 PM"
    
    @staticmethod
    def _generate_caption(
        content_type: str, 
        onboarding: OnboardingResponse,
        release_date: Optional[datetime],
        posting_date: datetime.date,
        song_name: str = ""
    ) -> str:
        """Generate caption based on content type and context"""
        captions = {
            'behind_scenes': 'This is where it all starts 🎵 Sometimes the best songs come when you least expect them.',
            'music_snippets': 'New music coming soon ✨ Pre-save link in bio',
            'performance': 'This song hits different live ⚡️',
            'trends': 'Had to put my spin on this trend 🔥',
            'storytelling': 'The story behind this song means everything to me. Here\'s why...',
            'lifestyle': 'A day in my life as a musician 🎸',
            'educational': 'Here\'s how I [create/produce/write] - hope this helps!'
        }
        
        base_caption = captions.get(content_type, 'New content coming your way ✨')
        
        # Add release context if applicable
        if release_date:
            days_until = (release_date.date() - posting_date).days
            if 0 <= days_until <= 14:
                if song_name:
                    base_caption += f' "{song_name}" drops in {days_until} days - link in bio to pre-save!'
                else:
                    base_caption += f' New release drops in {days_until} days - link in bio to pre-save!'
        
        return base_caption
    
    @staticmethod
    def _generate_hashtags(content_type: str, genre: str, inspiring_artists: str) -> List[str]:
        """Generate mix of broad and niche hashtags"""
        base_tags = ['newmusic', 'music', 'indie', 'artist', 'musician']
        
        genre_tags = []
        if genre:
            genre_lower = genre.lower().replace(' ', '')
            genre_tags = [genre_lower, f'{genre_lower}music']
        
        type_tags = {
            'behind_scenes': ['behindthescenes', 'studio', 'musicproduction'],
            'music_snippets': ['newsong', 'newrelease', 'musicpreview'],
            'performance': ['live', 'acoustic', 'performance'],
            'trends': ['fyp', 'viral', 'trending'],
            'storytelling': ['songwriting', 'musicstory', 'artistlife'],
            'lifestyle': ['artistlife', 'dayinthelife', 'musicianlife'],
            'educational': ['musictips', 'productiontips', 'musicadvice']
        }
        
        tags = base_tags + genre_tags + type_tags.get(content_type, [])
        
        # Limit to 15 hashtags
        return tags[:15]
    
    @staticmethod
    def generate_schedule_summary(schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of the schedule"""
        total_items = len(schedule)
        platforms = {}
        formats = {}
        activities = {'filming': 0, 'editing': 0, 'posting': 0}
        
        for item in schedule:
            platform = item.get('platform', 'unknown')
            format_type = item.get('format', 'unknown')
            activity = item.get('activity_type', 'unknown')
            
            platforms[platform] = platforms.get(platform, 0) + 1
            formats[format_type] = formats.get(format_type, 0) + 1
            if activity in activities:
                activities[activity] += 1
        
        return {
            'total_items': total_items,
            'posts_by_platform': platforms,
            'posts_by_format': formats,
            'activities': activities
        }
