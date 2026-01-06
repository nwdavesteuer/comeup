# Testing Instructions - How to Run and Test the Onboarding

## Step-by-Step Guide

### Step 1: Start the Backend Server

Open your terminal and run:

```bash
cd /Users/jonahsteuer/Documents/GitHub/comeup
source venv/bin/activate
python -m backend.main
```

**What to expect:**
- You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`
- The backend API is now running
- **Keep this terminal window open** - don't close it

### Step 2: Set Up Database

Open a **NEW terminal window** (keep the backend running in the first one) and run:

```bash
cd /Users/jonahsteuer/Documents/GitHub/comeup
source venv/bin/activate

# Delete existing database if it has errors (we'll recreate it)
rm -f fanbase_builder.db

# Run migrations to create all tables
alembic upgrade head

# Create migration for onboarding table (if it doesn't exist yet)
alembic revision --autogenerate -m "Add onboarding model"
alembic upgrade head
```

**What this does:**
- Deletes the old database (fresh start)
- Creates all base tables (users, artists, etc.)
- Creates the onboarding_responses table

**If you see "Target database is not up to date" error:**
- The migration file has been fixed, so just delete the database and run `alembic upgrade head` again

### Step 3: Install Node.js (If Not Already Installed)

**Check if you have Node.js:**
```bash
node --version
npm --version
```

**If you get "command not found":**
- **Option 1 (Easiest):** Download from https://nodejs.org/ (get the LTS version)
- **Option 2:** If you have Homebrew: `brew install node`
- See `FRONTEND_SETUP.md` for detailed instructions

**After installing Node.js, restart your terminal and verify:**
```bash
node --version
npm --version
```

### Step 4: Install Frontend Dependencies (First Time Only)

In the same new terminal window (or another new one), run:

```bash
cd /Users/jonahsteuer/Documents/GitHub/comeup/frontend
npm install
```

This installs React and all frontend dependencies. **Only need to do this once.**

### Step 5: Start the Frontend Development Server

**IMPORTANT:** Make sure you're in the `frontend` directory!

```bash
cd /Users/jonahsteuer/Documents/GitHub/comeup/frontend
npm run dev
```

**If you get "package.json not found" error:**
- You're in the wrong directory
- Run `cd frontend` first, then `npm run dev`

**What to expect:**
- You should see something like: `Local: http://localhost:5173/`
- The frontend is now running
- **Keep this terminal window open too**

### Step 6: Open Your Web Browser

1. Open any web browser (Chrome, Safari, Firefox, etc.)
2. Go to this URL: **http://localhost:5173**
3. You should see the Fanbase Builder login page

### Step 7: Test the Onboarding Flow

1. **Sign Up:**
   - Click "Sign up" or go to http://localhost:5173/signup
   - Enter:
     - Email: `test@example.com`
     - Password: `testpassword123`
     - Artist Name: `Test Artist`
     - Genre: (optional)
   - Click "Sign Up"
   - You'll be automatically redirected to the onboarding page

2. **Complete Onboarding:**
   - Answer each question one at a time
   - Click "Next" after each answer
   - Watch the progress bar fill up
   - After all 9 questions, click "Complete Onboarding"
   - You'll be redirected to the dashboard

## What You Should See

### When Backend is Running:
- Terminal shows: `INFO: Uvicorn running on http://0.0.0.0:8000`
- You can test the API at: http://localhost:8000/docs

### When Frontend is Running:
- Terminal shows: `Local: http://localhost:5173/`
- Browser shows: The Fanbase Builder login page

## Troubleshooting

**"Port already in use" error:**
- Backend: Change port in `backend/main.py` or kill the process using port 8000
- Frontend: Change port in `frontend/vite.config.js` or kill the process using port 5173

**"npm: command not found" or "node: command not found":**
- **You need to install Node.js first!**
- See `FRONTEND_SETUP.md` for detailed installation instructions
- Or download from https://nodejs.org/ (get the LTS version)
- After installing, restart your terminal and try again

**Frontend can't connect to backend:**
- Make sure backend is running on port 8000
- Check that `frontend/vite.config.js` has the correct proxy target

**Database errors:**
- Make sure you ran the migration: `alembic upgrade head`
- Check that SQLite database file exists: `ls -la fanbase_builder.db`

## Quick Reference

**Backend URL:** http://localhost:8000
**Frontend URL:** http://localhost:5173
**API Docs:** http://localhost:8000/docs

**To stop servers:**
- Press `Ctrl+C` in each terminal window

