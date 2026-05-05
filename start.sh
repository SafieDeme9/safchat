#!/bin/bash
# start.sh - Simple launcher

echo "🚀 Starting Italian Bot"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ Python not found! Install Python first."
    exit 1
fi

# Check if token is set
if grep -q "^TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE" .env 2>/dev/null; then
    echo "❌ Please set your TELEGRAM_TOKEN in .env (still has placeholder value)"
    exit 1
elif ! grep -q "^TELEGRAM_TOKEN=" .env 2>/dev/null; then
    echo "❌ TELEGRAM_TOKEN not found in .env"
    exit 1
else
    echo "✅ Token configured"
fi

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON -m venv venv
    echo "📦 Installing dependencies..."
    venv/bin/pip install -r requirements.txt
fi

# Run the bot
echo "🤖 Starting bot..."
venv/bin/python main.py