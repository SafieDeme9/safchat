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
if ! grep -q "TELEGRAM_TOKEN" .env; then
    echo "✅ Token seems configured"
else
    echo "❌ Please set your TELEGRAM_TOKEN in .env"
    exit 1
fi

# Install requirements if needed
if [ ! -d "venv" ]; then
    echo "📦 Installing dependencies..."
    $PYTHON -m pip install -r requirements.txt
fi

# Run the bot
echo "🤖 Starting bot..."
$PYTHON main.py