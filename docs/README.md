# Fanbase Builder - Multi-Artist Music Marketing Platform

A multi-tenant SaaS platform where independent music artists can connect their Spotify/Instagram/TikTok/YouTube accounts, view unified analytics, get AI-powered content recommendations, schedule posts, and receive predictive insights about what content will drive streaming growth.

## 🚀 Project Status

**Current Phase:** Initial Setup - Foundation
- ✅ Project structure created
- ⏳ Database models (in progress)
- ⏳ Authentication system
- ⏳ OAuth integrations

## 📋 Tech Stack

**Backend:**
- Python 3.11+
- FastAPI (REST API framework)
- SQLite (local dev) / PostgreSQL (production)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- APScheduler (scheduled background jobs)

**AI/ML:**
- Claude API (insights generation)
- scikit-learn (predictive models)
- pandas (data processing)

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Git
- (Optional) PostgreSQL for production deployment (see [DEPLOYMENT.md](./DEPLOYMENT.md))

### Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd fanbase-builder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Database Setup**
   
   **For Local Development (SQLite - No Installation Needed):**
   - The default `.env` uses SQLite - no setup required!
   - Database file will be created automatically at `fanbase_builder.db`
   
   **For Production (PostgreSQL):**
   - See [DEPLOYMENT.md](./DEPLOYMENT.md) for PostgreSQL setup options
   - Update `DATABASE_URL` in `.env` when ready to deploy

7. **Run the application**
   ```bash
   cd backend
   python main.py
   # Or: uvicorn main:app --reload
   ```

8. **Verify it's working**
   - Visit http://localhost:8000
   - Visit http://localhost:8000/docs for API documentation

## 📁 Project Structure

```
fanbase-builder/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API route handlers
│   ├── services/           # Business logic
│   ├── jobs/               # Background scheduled jobs
│   └── utils/               # Utility functions
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔐 Environment Variables

Key variables needed in `.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT token secret (generate a secure random string)
- `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET` - Spotify API credentials
- `ANTHROPIC_API_KEY` - Claude API key

See `.env.example` for full list.

## 🎯 Next Steps

1. **Create database models** (users, artists, connections, metrics, content)
2. **Set up Alembic migrations**
3. **Implement JWT authentication**
4. **Create OAuth integration for Spotify**
5. **Build basic API endpoints**

## 📚 Documentation

- [Architecture Summary](./cursor_setup_instructions.md)
- [Project Vision](./jonah_music_marketing_system_1.md)

## 🤝 Development Workflow

1. Create feature branch
2. Make changes
3. Test locally
4. Commit and push
5. Create PR (when ready)

## 📝 License

Private project - All rights reserved
