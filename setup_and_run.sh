#!/bin/bash
# Setup and run script for Fanbase Builder
# This script helps you get the prototype running quickly

set -e  # Exit on error

echo "🚀 Fanbase Builder - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "1️⃣ Checking Python version..."
python3 --version || { echo "❌ Python 3 not found!"; exit 1; }

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "2️⃣ Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "2️⃣ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "3️⃣ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "4️⃣ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "5️⃣ Creating .env file from defaults..."
    echo "   (Using SQLite for local development - no setup needed)"
    touch .env
    echo "✅ .env file created (using defaults)"
else
    echo "5️⃣ .env file already exists"
fi

# Check if migrations exist
if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions)" ]; then
    echo ""
    echo "6️⃣ Generating database migrations..."
    alembic revision --autogenerate -m "Initial schema"
    echo "✅ Migration generated"
else
    echo "6️⃣ Migrations already exist"
fi

# Run migrations
echo ""
echo "7️⃣ Running database migrations..."
alembic upgrade head
echo "✅ Database initialized"

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python -m backend.main"
echo ""
echo "Or use uvicorn directly:"
echo "  uvicorn backend.main:app --reload"
echo ""
echo "Then visit:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""

