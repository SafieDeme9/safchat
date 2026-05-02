# Safchat

A simple Telegram chatbot that uses a self-hosted Ollama model for AI responses and serves Italian proverbs.

## Features

- Telegram bot built with `python-telegram-bot`
- Loads configuration from `.env`
- Uses a local Ollama service for AI behavior (lightweight `qwen2.5:0.5b` model optimized for RPi 4)
- Supports commands like `/start`, `/proverb`, `/tip`, `/clear`, and `/status`

## Setup

1. Create a `.env` file in the project root.
2. Add your bot token and Ollama host settings:
   ```dotenv
   bot_token=YOUR_TELEGRAM_BOT_TOKEN
   OLLAMA_HOST=http://ollama:11434
   ENVIRONMENT=development
   ```
3. Install dependencies:
   ```bash
   source ./bin/activate
   pip install -r requirements.txt
   ```

## Run locally

```bash
python main.py
```

## Run with Docker Compose

```bash
sudo docker-compose up -d --build
```

## Notes

- The bot token must be valid and provided via `.env`
- The Ollama service should be available on the configured host
