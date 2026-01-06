# Quick Start Guide - Testing the Prototype

This guide will help you get the prototype running and start testing it.

## Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Set Up Environment Variables

The app will work with default settings for basic testing. Create a `.env` file if you want to customize:

```bash
cp .env.example .env
# Edit .env if needed (optional for basic testing)
```

**Note:** For basic API testing, you don't need any API keys. The app will use SQLite by default.

## Step 3: Initialize Database

Generate and run the database migrations:

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration to create tables
alembic upgrade head
```

## Step 4: Start the Server

```bash
python -m backend.main
```

Or using uvicorn directly:

```bash
uvicorn backend.main:app --reload
```

The server will start at `http://localhost:8000`

## Step 5: Test the API

### Option A: Use the Interactive API Docs (Recommended)

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser!

### Option B: Use curl or Postman

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Sign Up a New User
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "artist_name": "Test Artist"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

Save the `access_token` from the response!

#### Get Your Profile (Protected Route)
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

#### Get Metrics Overview
```bash
curl http://localhost:8000/api/metrics/overview \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## Testing Checklist

- [ ] Server starts without errors
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Can sign up a new user
- [ ] Can login and get access token
- [ ] Can access protected routes with token
- [ ] API docs load at `/docs`

## What Works Without API Keys

✅ User authentication (signup, login)
✅ Artist profile management
✅ Content management (create, list, update posts)
✅ Basic metrics endpoints (will return empty data)
✅ Database operations

## What Requires API Keys

❌ OAuth connections (Spotify, Instagram, TikTok, YouTube)
❌ AI features (Claude API)
❌ Actual platform data syncing

## Next Steps

1. Test the authentication flow
2. Create some test content posts
3. Explore the API documentation
4. Set up API keys when ready to test OAuth integrations

## Troubleshooting

**Database errors?**
- Make sure you ran `alembic upgrade head`
- Check that SQLite file was created: `ls -la fanbase_builder.db`

**Import errors?**
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Check you're using Python 3.9+

**Port already in use?**
- Change the port: `uvicorn backend.main:app --reload --port 8001`

