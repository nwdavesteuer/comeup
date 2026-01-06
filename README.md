# Fanbase Builder - Multi-Artist Music Marketing Platform

A multi-tenant SaaS platform where independent music artists can connect their Spotify/Instagram/TikTok/YouTube accounts, view unified analytics, get AI-powered content recommendations, schedule posts, and receive predictive insights about what content will drive streaming growth.

## Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (REST API framework)
- PostgreSQL (multi-tenant database) or SQLite (local development)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- APScheduler (scheduled background jobs)

**AI/ML:**
- Claude API (via Anthropic SDK) for insights generation
- scikit-learn for predictive models

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- Spotify API credentials
- Instagram/Facebook API credentials
- TikTok API credentials
- YouTube API credentials
- Claude API key (for AI features)
- Database URL (use SQLite for local dev, PostgreSQL for production)

### 3. Initialize Database

For SQLite (local development):
```bash
# Database will be created automatically on first run
python -m backend.main
```

For PostgreSQL (production):
```bash
# Create database first
createdb artist_platform

# Run migrations
alembic upgrade head
```

### 4. Run the Application

```bash
python -m backend.main
```

Or using uvicorn directly:
```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── config.py               # Configuration (env vars)
├── database.py             # Database connection setup
│
├── models/                 # SQLAlchemy models
│   ├── user.py
│   ├── artist.py
│   ├── connection.py
│   ├── metric.py
│   ├── content.py
│   ├── experiment.py
│   └── prediction.py
│
├── schemas/                # Pydantic schemas (request/response)
│   ├── auth.py
│   ├── artist.py
│   ├── connection.py
│   ├── metric.py
│   ├── content.py
│   └── ai.py
│
├── routers/                # API route handlers
│   ├── auth.py
│   ├── connections.py
│   ├── metrics.py
│   ├── content.py
│   └── ai.py
│
├── services/               # Business logic
│   ├── auth_service.py
│   ├── spotify_service.py
│   ├── instagram_service.py
│   ├── tiktok_service.py
│   ├── youtube_service.py
│   ├── insights_service.py
│   └── prediction_service.py
│
├── jobs/                   # Background scheduled jobs
│   ├── data_sync.py
│   ├── publishing.py
│   └── insights.py
│
└── utils/                  # Utility functions
    ├── auth.py
    ├── encryption.py
    └── oauth.py
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

### Platform Connections
- `GET /api/connect/{platform}` - Get OAuth URL (spotify, instagram, tiktok, youtube)
- `GET /api/callback/{platform}` - OAuth callback handler
- `GET /api/connections` - List connected platforms
- `DELETE /api/connections/{platform}` - Disconnect platform

### Metrics & Analytics
- `GET /api/metrics/overview` - Dashboard summary
- `GET /api/metrics/platform/{platform}` - Platform-specific metrics
- `GET /api/metrics/growth` - Growth trends

### Content Management
- `GET /api/content` - List all content
- `POST /api/content` - Create/schedule new post
- `GET /api/content/{post_id}` - Get post details
- `PUT /api/content/{post_id}` - Update post
- `DELETE /api/content/{post_id}` - Delete post
- `GET /api/content/calendar` - Calendar view
- `GET /api/content/{post_id}/performance` - Performance data

### AI Features
- `POST /api/ai/generate-ideas` - Generate content ideas
- `POST /api/ai/generate-caption` - Generate caption variations
- `POST /api/ai/weekly-insights` - Get weekly strategic insights
- `POST /api/ai/predict-performance` - Predict post performance

## Background Jobs

The application runs three scheduled background jobs:

1. **Daily Data Sync** (2 AM daily)
   - Refreshes OAuth tokens if needed
   - Pulls latest metrics from all connected platforms
   - Stores data in `daily_metrics` table

2. **Publishing Queue** (Every 5 minutes)
   - Finds scheduled posts ready to publish
   - Publishes to platform APIs
   - Updates post status

3. **Weekly Insights** (Monday at 8 AM)
   - Generates AI-powered insights for each artist
   - Analyzes last week's performance

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black backend/
isort backend/
```

## Multi-Tenancy

The platform is designed with multi-tenancy from day one. Every database query is automatically filtered by `artist_id` using FastAPI dependency injection. This ensures complete data isolation between artists.

## Security

- JWT tokens for authentication
- Encrypted OAuth tokens in database
- Password hashing with bcrypt
- CORS middleware configured
- All queries filtered by artist_id

## Production Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Set up reverse proxy (nginx)
5. Use process manager (systemd, supervisor, etc.)
6. Configure SSL/TLS certificates

See `DEPLOYMENT.md` for detailed deployment instructions.

## License

MIT

