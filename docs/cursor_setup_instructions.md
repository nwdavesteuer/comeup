# Multi-Artist Music Marketing Platform - Architecture Summary for Cursor

## Project Overview
Build a multi-tenant SaaS platform where independent music artists can connect their Spotify/Instagram/TikTok/YouTube accounts, view unified analytics, get AI-powered content recommendations, schedule posts, and receive predictive insights about what content will drive streaming growth.

---

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (REST API framework)
- PostgreSQL (multi-tenant database)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- APScheduler (scheduled background jobs)
- Redis (task queue, caching - optional for MVP)

**Frontend:**
- React + TypeScript (OR Streamlit for faster MVP)
- Tailwind CSS
- Recharts/Chart.js for visualizations

**AI/ML:**
- Claude API (via Anthropic SDK) for insights generation
- scikit-learn for predictive models
- pandas for data processing

**Infrastructure:**
- AWS S3 (media storage)
- Railway or Render (deployment)
- GitHub (version control)

---

## Database Schema (PostgreSQL Multi-Tenant)

### Core Tables

```sql
-- User Authentication
users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    last_login TIMESTAMP
)

-- Artist Accounts
artists (
    artist_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    artist_name VARCHAR(255),
    genre VARCHAR(100),
    subscription_tier VARCHAR(50), -- 'free', 'pro', 'premium'
    onboarding_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP
)

-- Platform Connections (OAuth tokens)
platform_connections (
    connection_id UUID PRIMARY KEY,
    artist_id UUID REFERENCES artists(artist_id),
    platform VARCHAR(50), -- 'spotify', 'instagram', 'tiktok', 'youtube'
    access_token TEXT, -- encrypted
    refresh_token TEXT, -- encrypted
    token_expires_at TIMESTAMP,
    connected_at TIMESTAMP,
    last_sync TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
)

-- Daily Metrics (time-series data)
daily_metrics (
    metric_id UUID PRIMARY KEY,
    artist_id UUID REFERENCES artists(artist_id), -- CRITICAL: always filter by this
    date DATE NOT NULL,
    platform VARCHAR(50),
    metric_name VARCHAR(100), -- 'monthly_listeners', 'followers', 'streams', etc.
    value BIGINT,
    created_at TIMESTAMP,
    UNIQUE(artist_id, date, platform, metric_name)
)
CREATE INDEX idx_daily_metrics_artist_date ON daily_metrics(artist_id, date);

-- Content Posts
content_posts (
    post_id UUID PRIMARY KEY,
    artist_id UUID REFERENCES artists(artist_id),
    platform VARCHAR(50),
    content_type VARCHAR(50), -- 'reel', 'story', 'tiktok', 'youtube_short', 'post'
    caption TEXT,
    media_url TEXT,
    external_url TEXT, -- link to actual post on platform
    posted_at TIMESTAMP,
    scheduled_for TIMESTAMP,
    status VARCHAR(50), -- 'draft', 'scheduled', 'published', 'failed'
    created_at TIMESTAMP
)
CREATE INDEX idx_content_posts_artist ON content_posts(artist_id, posted_at);

-- Content Performance (tracked over time)
content_performance (
    performance_id UUID PRIMARY KEY,
    post_id UUID REFERENCES content_posts(post_id),
    artist_id UUID REFERENCES artists(artist_id),
    measured_at TIMESTAMP,
    likes INTEGER,
    comments INTEGER,
    shares INTEGER,
    saves INTEGER,
    impressions INTEGER,
    reach INTEGER,
    engagement_rate DECIMAL(5,4),
    spotify_traffic_lift INTEGER, -- streams increase in 48hr window
    created_at TIMESTAMP
)

-- Experiments (A/B tests)
experiments (
    experiment_id UUID PRIMARY KEY,
    artist_id UUID REFERENCES artists(artist_id),
    name VARCHAR(255),
    hypothesis TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50), -- 'active', 'completed', 'cancelled'
    results JSONB, -- store statistical results
    created_at TIMESTAMP
)

-- Predictions Cache (store ML predictions)
predictions (
    prediction_id UUID PRIMARY KEY,
    artist_id UUID REFERENCES artists(artist_id),
    post_id UUID REFERENCES content_posts(post_id),
    prediction_type VARCHAR(50), -- 'engagement_rate', 'streams_lift', 'viral_probability'
    predicted_value DECIMAL(10,4),
    confidence_score DECIMAL(5,4),
    created_at TIMESTAMP
)
```

---

## API Architecture

### Authentication Layer
```
POST /api/auth/signup
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

### Platform Connections (OAuth flows)
```
GET  /api/connect/spotify        → Generate Spotify OAuth URL
GET  /api/connect/instagram      → Generate Instagram OAuth URL
GET  /api/connect/tiktok         → Generate TikTok OAuth URL
GET  /api/connect/youtube        → Generate YouTube OAuth URL

GET  /api/callback/spotify?code={code}&state={artist_id}
GET  /api/callback/instagram?code={code}&state={artist_id}
GET  /api/callback/tiktok?code={code}&state={artist_id}
GET  /api/callback/youtube?code={code}&state={artist_id}

GET  /api/connections            → List artist's connected platforms
DELETE /api/connections/{platform} → Disconnect platform
```

### Metrics & Analytics
```
GET  /api/metrics/overview              → Dashboard summary
GET  /api/metrics/platform/{platform}   → Platform-specific metrics
GET  /api/metrics/growth                → Growth trends
GET  /api/metrics/attribution           → Social content → streaming attribution
```

### Content Management
```
GET    /api/content                     → List all content
POST   /api/content                     → Create/schedule new post
GET    /api/content/{post_id}           → Get post details
PUT    /api/content/{post_id}           → Update post
DELETE /api/content/{post_id}           → Delete post
GET    /api/content/calendar            → Calendar view
GET    /api/content/performance/{post_id} → Performance data
```

### AI Features
```
POST /api/ai/generate-ideas             → Generate content ideas
POST /api/ai/generate-caption           → Generate caption variations
POST /api/ai/weekly-insights            → Get weekly strategic insights
POST /api/ai/predict-performance        → Predict post performance
```

### Experiments
```
GET  /api/experiments                   → List experiments
POST /api/experiments                   → Create experiment
GET  /api/experiments/{experiment_id}   → Get results
```

---

## Background Jobs (APScheduler)

### Daily Data Sync Job
```python
@scheduler.scheduled_job('cron', hour=2, minute=0)  # 2 AM daily
async def sync_all_artists_data():
    """
    For each artist with active platform connections:
    1. Refresh OAuth tokens if needed
    2. Pull latest metrics from Spotify/Instagram/TikTok/YouTube
    3. Store in daily_metrics table
    4. Calculate growth rates
    5. Update content_performance for recent posts
    """
```

### Publishing Queue Job  
```python
@scheduler.scheduled_job('interval', minutes=5)
async def process_publishing_queue():
    """
    Every 5 minutes:
    1. Find posts with status='scheduled' and scheduled_for <= now + 5 min
    2. Publish to platform APIs
    3. Update status to 'published'
    4. Start tracking performance
    """
```

### Weekly Insights Job
```python
@scheduler.scheduled_job('cron', day_of_week='mon', hour=8)
async def generate_weekly_insights():
    """
    Every Monday at 8 AM:
    1. Analyze last week's data for each artist
    2. Use Claude API to generate strategic insights
    3. Email insights to artist
    4. Store in database for dashboard view
    """
```

---

## Key Architectural Patterns

### 1. Multi-Tenancy (Data Isolation)
```python
# Every database query MUST filter by artist_id
# Use FastAPI dependency injection to enforce this

from fastapi import Depends

async def get_current_artist(token: str = Depends(oauth2_scheme)) -> Artist:
    """Verify JWT token and return artist context"""
    payload = jwt.decode(token, SECRET_KEY)
    artist = db.query(Artist).filter(Artist.artist_id == payload['artist_id']).first()
    return artist

# All endpoints require artist context
@app.get("/api/metrics/overview")
async def get_metrics(artist: Artist = Depends(get_current_artist)):
    # This query is automatically scoped to this artist
    metrics = db.query(DailyMetric).filter(
        DailyMetric.artist_id == artist.artist_id
    ).all()
    return metrics
```

### 2. OAuth Integration Pattern
```python
# OAuth flow for each platform
class SpotifyOAuth:
    def get_auth_url(self, artist_id: str) -> str:
        """Generate OAuth URL with state parameter"""
        state = jwt.encode({'artist_id': artist_id}, SECRET_KEY)
        return f"{SPOTIFY_AUTH_URL}?client_id={CLIENT_ID}&state={state}&..."
    
    async def handle_callback(self, code: str, state: str):
        """Exchange code for access token"""
        # Decode state to get artist_id
        payload = jwt.decode(state, SECRET_KEY)
        artist_id = payload['artist_id']
        
        # Exchange code for tokens
        tokens = await spotify_api.exchange_code(code)
        
        # Store encrypted tokens
        connection = PlatformConnection(
            artist_id=artist_id,
            platform='spotify',
            access_token=encrypt(tokens['access_token']),
            refresh_token=encrypt(tokens['refresh_token']),
            token_expires_at=datetime.now() + timedelta(seconds=tokens['expires_in'])
        )
        db.add(connection)
        db.commit()
```

### 3. External API Integration Layer
```python
# Abstraction for platform APIs
class PlatformAPIManager:
    
    async def sync_spotify_data(self, artist_id: UUID):
        """Fetch and store Spotify data"""
        connection = get_platform_connection(artist_id, 'spotify')
        
        # Refresh token if needed
        if connection.token_expires_at < datetime.now():
            await self.refresh_spotify_token(connection)
        
        # Fetch data
        data = await spotify_api.get_artist_stats(connection.access_token)
        
        # Store in database
        metric = DailyMetric(
            artist_id=artist_id,
            date=date.today(),
            platform='spotify',
            metric_name='monthly_listeners',
            value=data['monthly_listeners']
        )
        db.add(metric)
        db.commit()
    
    # Similar methods for instagram, tiktok, youtube
```

### 4. Predictive Models
```python
# ML prediction pipeline
class PerformancePredictor:
    
    def __init__(self):
        self.model = joblib.load('models/engagement_predictor.pkl')
    
    def predict_engagement(self, post_data: dict) -> dict:
        """Predict engagement rate for a post"""
        
        # Feature engineering
        features = self.extract_features(post_data)
        
        # Predict
        prediction = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features]).max()
        
        return {
            'predicted_engagement_rate': prediction,
            'confidence': confidence,
            'recommendation': self.generate_recommendation(prediction)
        }
    
    def extract_features(self, post_data: dict) -> list:
        """Convert post data to model features"""
        return [
            post_data['hour_of_day'],
            post_data['day_of_week'],
            post_data['caption_length'],
            post_data['has_hashtags'],
            post_data['content_type_encoded'],
            # ... more features
        ]
```

### 5. Claude API Integration
```python
# AI insights generation
class InsightsGenerator:
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    async def generate_weekly_insights(self, artist_id: UUID) -> str:
        """Generate strategic insights using Claude"""
        
        # Gather artist's data
        metrics = get_week_metrics(artist_id)
        content = get_week_content(artist_id)
        
        # Create prompt
        prompt = f"""
        Analyze this music artist's weekly performance:
        
        Metrics:
        - Spotify streams: {metrics['streams']} ({metrics['streams_growth']}% vs last week)
        - Instagram followers: {metrics['ig_followers']} ({metrics['ig_growth']}%)
        - TikTok views: {metrics['tiktok_views']}
        - Engagement rate: {metrics['engagement_rate']:.2%}
        
        Content posted: {len(content)} posts
        Top performer: {content[0].description}
        
        Provide:
        1. Three key insights about what's working
        2. Two specific action items for this week
        3. One experiment to test
        
        Be concise, actionable, and specific to this artist's data.
        """
        
        # Call Claude API
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
```

---

## File Structure

```
artist-marketing-platform/
│
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration (env vars, secrets)
│   ├── database.py             # Database connection setup
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── artist.py
│   │   ├── connection.py
│   │   ├── metric.py
│   │   └── content.py
│   │
│   ├── schemas/                # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── artist.py
│   │   └── content.py
│   │
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── connections.py
│   │   ├── metrics.py
│   │   ├── content.py
│   │   └── ai.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── spotify_service.py
│   │   ├── instagram_service.py
│   │   ├── tiktok_service.py
│   │   ├── youtube_service.py
│   │   ├── prediction_service.py
│   │   └── insights_service.py
│   │
│   ├── jobs/                   # Background scheduled jobs
│   │   ├── __init__.py
│   │   ├── data_sync.py
│   │   ├── publishing.py
│   │   └── insights.py
│   │
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── encryption.py
│   │   ├── oauth.py
│   │   └── ml_helpers.py
│   │
│   └── alembic/                # Database migrations
│       └── versions/
│
├── frontend/                   # React app (or use Streamlit for faster MVP)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── utils/
│   └── public/
│
├── ml_models/                  # Machine learning models
│   ├── train_engagement_predictor.py
│   ├── train_growth_forecaster.py
│   └── models/                 # Saved model files
│
├── tests/
│   ├── test_auth.py
│   ├── test_api.py
│   └── test_services.py
│
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore
├── README.md
└── docker-compose.yml         # Optional: for local development
```

---

## Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/artist_platform

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Spotify API
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=https://yourapp.com/callback/spotify

# Instagram/Facebook API
INSTAGRAM_APP_ID=your-instagram-app-id
INSTAGRAM_APP_SECRET=your-instagram-app-secret
INSTAGRAM_REDIRECT_URI=https://yourapp.com/callback/instagram

# TikTok API
TIKTOK_CLIENT_KEY=your-tiktok-client-key
TIKTOK_CLIENT_SECRET=your-tiktok-client-secret
TIKTOK_REDIRECT_URI=https://yourapp.com/callback/tiktok

# YouTube API
YOUTUBE_CLIENT_ID=your-youtube-client-id
YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
YOUTUBE_REDIRECT_URI=https://yourapp.com/callback/youtube

# Claude API
ANTHROPIC_API_KEY=your-anthropic-api-key

# AWS S3 (for media storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
S3_BUCKET_NAME=your-bucket-name

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## Key Dependencies (requirements.txt)

```
# Core
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# HTTP Clients
httpx==0.25.2
requests==2.31.0

# Scheduling
apscheduler==3.10.4

# Data Processing
pandas==2.1.3
numpy==1.26.2

# Machine Learning
scikit-learn==1.3.2
joblib==1.3.2

# AI
anthropic==0.7.8

# AWS
boto3==1.29.7

# Encryption
cryptography==41.0.7

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
```

---

## Cursor Prompts to Get Started

### Initial Project Setup
```
Create a multi-tenant SaaS platform for music artists with the following:

1. FastAPI backend with user authentication using JWT tokens
2. PostgreSQL database with multi-tenant architecture (all queries filtered by artist_id)
3. OAuth2 integration framework for Spotify, Instagram, TikTok, and YouTube
4. Proper project structure with routers, services, models, and schemas
5. Database migrations using Alembic
6. Environment variable configuration using python-dotenv
7. Basic CRUD endpoints for artists and platform connections

Requirements:
- Use SQLAlchemy ORM for database operations
- Implement proper data isolation (every query must filter by artist_id)
- Include password hashing with bcrypt
- Set up CORS middleware
- Create comprehensive README with setup instructions

File structure should follow best practices with separate folders for:
- models/ (SQLAlchemy models)
- schemas/ (Pydantic schemas)
- routers/ (API endpoints)
- services/ (business logic)
- utils/ (helper functions)
```

### Database Schema Setup
```
Create the PostgreSQL database schema for a multi-artist music marketing platform:

Tables needed:
1. users (user_id, email, password_hash, created_at)
2. artists (artist_id, user_id FK, artist_name, genre, subscription_tier, onboarding_complete)
3. platform_connections (connection_id, artist_id FK, platform, access_token encrypted, refresh_token encrypted, token_expires_at, connected_at, last_sync)
4. daily_metrics (metric_id, artist_id FK, date, platform, metric_name, value) - with index on (artist_id, date)
5. content_posts (post_id, artist_id FK, platform, content_type, caption, media_url, posted_at, scheduled_for, status)
6. content_performance (performance_id, post_id FK, artist_id FK, measured_at, likes, comments, shares, saves, impressions, engagement_rate, spotify_traffic_lift)
7. predictions (prediction_id, artist_id FK, post_id FK, prediction_type, predicted_value, confidence_score)

Use UUID for primary keys, proper foreign key relationships, and create indexes for performance.
Generate Alembic migration script.
```

### OAuth Integration
```
Implement OAuth2 integration for Spotify authentication:

1. Create /api/connect/spotify endpoint that generates OAuth URL with state parameter containing artist_id
2. Create /api/callback/spotify endpoint that:
   - Exchanges authorization code for access/refresh tokens
   - Decodes state parameter to get artist_id
   - Stores encrypted tokens in platform_connections table
   - Handles token expiration timestamps
   - Returns success response

Include proper error handling, token encryption/decryption utilities, and token refresh logic.

Use the Spotify Web API OAuth flow with authorization code grant type.
```

### Background Jobs
```
Create APScheduler background jobs for:

1. Daily data sync job (runs at 2 AM):
   - Query all artists with active platform connections
   - For each artist, refresh OAuth tokens if needed
   - Pull latest metrics from Spotify API
   - Store in daily_metrics table
   - Calculate growth rates
   - Handle errors gracefully (log but continue)

2. Publishing queue job (runs every 5 minutes):
   - Find posts with status='scheduled' and scheduled_for <= now + 5 minutes
   - Publish to platform APIs
   - Update status to 'published'
   - Track initial performance

Include proper error handling, logging, and retry logic.
```

---

## Next Steps After Initial Setup

1. **Week 1:** Get core platform working (auth, database, basic endpoints)
2. **Week 2:** Implement Spotify OAuth and data sync
3. **Week 3:** Add Instagram/TikTok integrations
4. **Week 4:** Build basic dashboard and metrics visualization
5. **Month 2:** Add AI features, predictions, content scheduling
6. **Month 3:** Polish, testing, deploy, onboard first artists

---

This architecture is designed to be:
- **Scalable:** Multi-tenant from day one
- **Secure:** Proper authentication, encrypted tokens, data isolation
- **Extensible:** Easy to add new platforms or features
- **Production-ready:** Proper separation of concerns, error handling, background jobs

The key is starting with the foundation (auth + database + one OAuth integration) and building incrementally from there.
