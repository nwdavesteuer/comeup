# Multi-Artist Music Marketing Platform - Architecture Summary for Cursor

## Week 0 Quick Start Guide

**This document supports the Week 0 checklist in the main spec.** Follow these steps in order:

### Step 1: Install Prerequisites (Day 1)
```bash
# Verify installations:
python --version   # Should be 3.11+
node --version     # Should be 18+
git --version      # Should be installed
```

### Step 2: Create GitHub Repository (Day 1)
```bash
# On GitHub.com, create: "artist-marketing-platform"
git clone https://github.com/YOUR_USERNAME/artist-marketing-platform.git
cd artist-marketing-platform
mkdir backend frontend
```

### Step 3: Backend Setup (Day 2-3)
See "Backend Setup with Cursor" section below for detailed prompts.

### Step 4: Frontend Setup (Day 4-5)
See "Frontend Setup with Cursor" section below for detailed prompts.

### Step 5: Deployment (Day 6-7)
See "Deployment Setup" section below for Railway and Vercel configuration.

---

## Project Overview
Build a multi-tenant SaaS platform where independent music artists can connect their Spotify/Instagram/TikTok/YouTube accounts, view unified analytics, get AI-powered content recommendations, schedule posts, and receive predictive insights about what content will drive streaming growth.

---

---

## Frontend Setup with Cursor

### Initial React Project Setup

Open Cursor in your `frontend/` directory and use this prompt:

```
Create a modern React application with TypeScript using Vite.

Setup requirements:

1. Initialize project with:
   - Vite as build tool (faster than create-react-app)
   - React 18+ with TypeScript
   - React Router v6 for navigation
   - Tailwind CSS for styling
   - Axios for HTTP requests

2. Project structure:
   frontend/
   ├── src/
   │   ├── main.tsx              # Entry point
   │   ├── App.tsx               # Main app component
   │   ├── components/           # Reusable components
   │   │   ├── Navbar.tsx
   │   │   └── LoadingSpinner.tsx
   │   ├── pages/                # Page components
   │   │   ├── Login.tsx
   │   │   ├── Dashboard.tsx
   │   │   └── NotFound.tsx
   │   ├── services/             # API service layer
   │   │   └── api.ts            # Axios configuration
   │   ├── hooks/                # Custom React hooks
   │   │   └── useAuth.tsx       # Authentication hook
   │   ├── types/                # TypeScript types
   │   │   └── index.ts
   │   └── utils/                # Helper functions
   │       └── storage.ts        # LocalStorage helpers
   ├── public/
   ├── index.html
   ├── package.json
   ├── vite.config.ts
   ├── tsconfig.json
   ├── tailwind.config.js
   ├── postcss.config.js
   └── .env.example

3. Configure Vite with:
   - Proxy to backend API during development (avoid CORS)
   - Environment variables support
   - Hot module replacement

4. Setup Tailwind CSS with:
   - Base configuration
   - Custom colors if needed
   - Responsive breakpoints

5. Create basic API service with Axios:
   - Base URL from environment variable
   - Request/response interceptors for auth tokens
   - Error handling
   - Type-safe API calls

6. Setup React Router with:
   - Public routes (login)
   - Protected routes (dashboard)
   - 404 page
   - Route guards for authentication

7. Create basic components:
   - Login page with form
   - Dashboard page with test API call
   - Simple navigation bar
   - Loading spinner

8. Environment setup:
   - .env.example with VITE_API_URL
   - Instructions for local development

Generate all necessary configuration files and provide instructions for:
- Installing dependencies (npm install)
- Running dev server (npm run dev)
- Building for production (npm run build)
- Testing the setup
```

### API Service Configuration

The generated `src/services/api.ts` should look like this:

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
export const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor - add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/api/auth/login', { email, password }),
  
  signup: (email: string, password: string, artistName: string) =>
    api.post('/api/auth/signup', { email, password, artist_name: artistName }),
  
  me: () => api.get('/api/auth/me'),
};

export const metricsAPI = {
  getOverview: () => api.get('/api/metrics/overview'),
  
  getPlatformMetrics: (platform: string) =>
    api.get(`/api/metrics/platform/${platform}`),
};

// Health check for testing
export const healthCheck = () => api.get('/health');
```

### Dashboard Component with Backend Test

Create a test dashboard that proves frontend↔backend connection:

```
Create a Dashboard component that:

1. Displays a header "Artist Dashboard"

2. On component mount, calls the backend health check endpoint

3. Shows loading state while fetching

4. Displays backend status:
   - If successful: "✓ Connected to backend" in green
   - If error: "✗ Backend connection failed" in red with error message

5. Includes a button "Test API" that calls /api/metrics/overview

6. Uses Tailwind CSS for styling

7. Includes proper TypeScript types

8. Handles loading and error states gracefully

Example structure:
- Loading spinner while fetching
- Success/error messages with icons
- Clean card layout with Tailwind
- Button with hover states
```

### Environment Configuration

Create `.env.example`:
```
VITE_API_URL=http://localhost:8000
```

Create `.env.local` (not committed):
```
VITE_API_URL=http://localhost:8000
```

For production (set in Vercel):
```
VITE_API_URL=https://your-backend.railway.app
```

### Vite Configuration for Development Proxy

Update `vite.config.ts` to proxy API calls during development:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

This allows frontend at `localhost:5173` to call backend at `localhost:8000` without CORS issues during development.

### Running Frontend Locally

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Run development server
npm run dev

# Should start at http://localhost:5173
```

Test checklist:
- [ ] Can access http://localhost:5173
- [ ] Dashboard loads
- [ ] "Test API" button calls backend successfully
- [ ] No CORS errors in console
- [ ] Backend status shows as connected

---

## Deployment Setup

### Backend Deployment to Railway

**Option 1: Railway CLI (Recommended)**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# In backend directory
cd backend

# Initialize Railway project
railway init

# Link to your GitHub repo
railway link

# Add PostgreSQL database
railway add postgresql

# Deploy
railway up

# Get deployment URL
railway domain
```

**Option 2: Railway Dashboard (Easier for beginners)**

1. Go to https://railway.app and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `artist-marketing-platform` repository
4. Railway detects Python automatically
5. Click "Add Plugin" → "PostgreSQL"
6. Configure environment variables in Railway dashboard:
   - `DATABASE_URL` (auto-populated by Railway)
   - `SECRET_KEY` (generate with: `openssl rand -hex 32`)
   - `ANTHROPIC_API_KEY` (your Claude API key)
   - Add any OAuth keys (SPOTIFY_CLIENT_ID, etc.)

7. Railway automatically:
   - Installs dependencies from requirements.txt
   - Runs database migrations
   - Starts your FastAPI app
   - Provides HTTPS URL

8. Get your URL: `https://your-app.up.railway.app`

**Railway Configuration Files**

Create `railway.toml` in backend directory:
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

**Automatic Deployments**

Railway watches your GitHub repository:
- Push to `main` → Automatic deployment
- Pull request → Preview deployment
- See logs in Railway dashboard

**Testing Backend Deployment**

```bash
# Test health endpoint
curl https://your-app.up.railway.app/health

# Should return:
# {"status":"healthy","database":"connected"}
```

---

### Frontend Deployment to Vercel

**Option 1: Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# In frontend directory
cd frontend

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: artist-marketing-platform
# - Directory: ./
# - Override build settings? No

# Deploy to production
vercel --prod
```

**Option 2: Vercel Dashboard (Recommended)**

1. Go to https://vercel.com and sign in with GitHub

2. Click "Add New" → "Project"

3. Import `artist-marketing-platform` repository

4. Configure build settings:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

5. Add Environment Variables:
   - Name: `VITE_API_URL`
   - Value: `https://your-backend.up.railway.app` (your Railway URL)

6. Click "Deploy"

7. Vercel will:
   - Install dependencies
   - Build your React app
   - Deploy to global CDN
   - Provide HTTPS URL

8. Get your URL: `https://your-app.vercel.app`

**Vercel Configuration File**

Create `vercel.json` in frontend directory:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**Automatic Deployments**

Vercel watches your GitHub repository:
- Push to `main` → Production deployment
- Push to other branches → Preview deployment
- Pull requests → Preview URLs for review
- See logs and analytics in Vercel dashboard

**Testing Frontend Deployment**

1. Visit `https://your-app.vercel.app`
2. Dashboard should load
3. Click "Test API" button
4. Should successfully call Railway backend
5. Check browser console for any CORS errors

---

### CORS Configuration for Production

**Update Backend CORS settings** in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

# Get allowed origins from environment variable
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        FRONTEND_URL,              # Production frontend
        "https://*.vercel.app",   # Vercel preview URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Add FRONTEND_URL to Railway environment variables:**
- `FRONTEND_URL=https://your-app.vercel.app`

---

### GitHub Actions for CI/CD (Optional but Recommended)

Create `.github/workflows/backend-tests.yml`:

```yaml
name: Backend Tests

on:
  push:
    branches: [ main ]
    paths:
      - 'backend/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      working-directory: ./backend
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      working-directory: ./backend
      run: pytest
```

Create `.github/workflows/frontend-tests.yml`:

```yaml
name: Frontend Tests

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      working-directory: ./frontend
      run: npm ci
    
    - name: Build
      working-directory: ./frontend
      run: npm run build
```

---

### Complete Week 0 Deployment Checklist

**Backend (Railway):**
- [ ] Created Railway account
- [ ] Connected GitHub repository
- [ ] Railway detected Python project
- [ ] PostgreSQL database added
- [ ] Environment variables configured
- [ ] Deployment successful
- [ ] Health check endpoint works: `curl https://your-app.railway.app/health`

**Frontend (Vercel):**
- [ ] Created Vercel account
- [ ] Connected GitHub repository
- [ ] Build settings configured (Vite, frontend root)
- [ ] VITE_API_URL environment variable set to Railway URL
- [ ] Deployment successful
- [ ] Can access site: `https://your-app.vercel.app`
- [ ] Frontend successfully calls backend (no CORS errors)

**Automatic Deployments:**
- [ ] Push to main → Railway deploys backend automatically
- [ ] Push to main → Vercel deploys frontend automatically
- [ ] Can see deployment logs in both dashboards
- [ ] Deployment typically completes in 1-2 minutes

**End-to-End Test:**
- [ ] Visit production frontend URL
- [ ] Dashboard loads successfully
- [ ] Backend status shows "Connected"
- [ ] Can click "Test API" button successfully
- [ ] Browser console shows no errors
- [ ] Share URL with someone else - they can access it

**If all checkboxes are complete:** ✅ Week 0 is done! Move to Week 1 (Authentication + OAuth)

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

## Week 0 Troubleshooting Guide

### Common Issues and Solutions

#### "Backend won't start - ModuleNotFoundError"

**Problem:** Missing Python dependencies

**Solution:**
```bash
cd backend
pip install -r requirements.txt

# If still failing, try:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

#### "Database connection failed"

**Problem:** PostgreSQL not running or wrong credentials

**Solution for Local Development:**
```bash
# Check if PostgreSQL is running
# On Mac:
brew services list | grep postgresql

# On Linux:
sudo systemctl status postgresql

# If not running, start it:
brew services start postgresql  # Mac
sudo systemctl start postgresql # Linux

# Test connection:
psql -U postgres -d artist_platform
```

**Solution for Railway:**
- Check DATABASE_URL environment variable is set
- Verify PostgreSQL plugin is added in Railway dashboard
- Check Railway logs for connection errors

---

#### "Frontend can't reach backend - CORS error"

**Problem:** Browser blocking requests due to CORS policy

**Symptoms:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**
Add CORS middleware to FastAPI `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### "Railway deployment failed"

**Problem:** Build or startup errors

**Solution:**
1. Check Railway logs (click on deployment in dashboard)
2. Common issues:
   - Missing requirements.txt
   - Wrong Python version (specify in runtime.txt: `python-3.11.5`)
   - Wrong start command
   - Missing environment variables

3. Verify `railway.toml` is correct

4. Check all environment variables are set in Railway dashboard

---

#### "Vercel build failed"

**Problem:** Frontend build errors

**Solution:**
1. Check build logs in Vercel dashboard
2. Test build locally first:
```bash
cd frontend
npm run build
# Should complete without errors
```

---

### Getting Help

**If you're stuck for more than 2 hours:**

1. **Use Cursor heavily** - Paste error messages directly
2. **Check Documentation** - FastAPI, Railway, Vercel docs
3. **Community Support** - Railway/Vercel Discord servers
4. **Stack Overflow** - Search for your exact error

**Remember:** Getting stuck is normal. Get unstuck quickly.

---

## Summary: Week 0 Success Path

1. **Day 1-2:** Install tools, create repo, understand architecture
2. **Day 3-4:** Backend setup with Cursor, deploy to Railway
3. **Day 5-6:** Frontend setup with Cursor, deploy to Vercel
4. **Day 7:** Test end-to-end, fix issues, verify auto-deployments

**Success = Working "hello world" app that:**
- Runs locally (frontend talks to backend)
- Deployed to production (accessible via URLs)
- Auto-deploys when you push to GitHub

**Once Week 0 works → Ready for Week 1: Authentication + OAuth**
