# Deployment Guide

## Development Setup (SQLite - No Installation Needed)

For local development, we use SQLite which requires no setup:

1. **Create `.env` file** (copy from `.env.example`)
2. **Use default DATABASE_URL** (already set to SQLite):
   ```
   DATABASE_URL=sqlite:///./fanbase_builder.db
   ```
3. **Run the app** - database file will be created automatically

## Production Setup (PostgreSQL)

When ready to deploy, you'll need PostgreSQL. Here are options:

### Option 1: Railway (Recommended - Easiest)

1. **Sign up at [railway.app](https://railway.app)**
2. **Create new project**
3. **Add PostgreSQL service** (Railway provides managed PostgreSQL)
4. **Copy the DATABASE_URL** from Railway's PostgreSQL service
5. **Add to your `.env`** or Railway environment variables

Railway automatically provides:
- PostgreSQL database
- Automatic backups
- Connection pooling
- Free tier available

### Option 2: Render

1. **Sign up at [render.com](https://render.com)**
2. **Create PostgreSQL database**
3. **Copy Internal Database URL**
4. **Add to environment variables**

### Option 3: Supabase (Free PostgreSQL)

1. **Sign up at [supabase.com](https://supabase.com)**
2. **Create new project**
3. **Go to Settings > Database**
4. **Copy Connection String** (use the URI format)
5. **Add to environment variables**

### Option 4: Local PostgreSQL (if you want to install)

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb artist_platform
```

**Update `.env`:**
```
DATABASE_URL=postgresql://$(whoami)@localhost:5432/artist_platform
```

## Switching from SQLite to PostgreSQL

When you're ready to deploy:

1. **Set up PostgreSQL** (using one of the options above)
2. **Update DATABASE_URL** in your `.env` or hosting environment variables
3. **Run migrations** to create tables:
   ```bash
   alembic upgrade head
   ```
4. **That's it!** The code automatically detects PostgreSQL vs SQLite

## Environment Variables for Production

Make sure to set these in your hosting platform:

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Generate a secure random string (never commit this!)
- `CORS_ORIGINS` - Your frontend URL(s)

**API Keys (as you add features):**
- `SPOTIFY_CLIENT_ID` / `SPOTIFY_CLIENT_SECRET`
- `ANTHROPIC_API_KEY`
- Other platform credentials

## Generating SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Deployment Checklist

- [ ] PostgreSQL database set up
- [ ] DATABASE_URL configured
- [ ] SECRET_KEY generated and set
- [ ] CORS_ORIGINS configured for your domain
- [ ] API keys added (Spotify, Claude, etc.)
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] App deployed and health check passing

## Notes

- **SQLite is fine for development** - no need to set up PostgreSQL until you're ready to deploy
- **The code automatically handles both** - just change DATABASE_URL
- **Railway is recommended** because it's the easiest and has a good free tier

