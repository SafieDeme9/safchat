# Safchat — AI Italian Tutor Telegram Bot

A Telegram bot that helps you learn Italian using the **DeepSeek API** (fast,
accurate, no local GPU needed). Can also fall back to a local Ollama model.

**What it does:**
- Translates English / French to Italian
- Corrects your Italian grammar and spelling
- Has simple conversations in Italian
- Sends random Italian proverbs (`/proverb`)
- Gives learning tips (`/tip`)

---

## Prerequisites

1. **Docker** and **Docker Compose** installed:
   ```bash
   apt install docker.io docker-compose-plugin -y
   ```

2. **Add your user to the `docker` group** (so you don't need `sudo`):
   ```bash
   sudo usermod -aG docker $USER && newgrp docker
   ```

3. **A Telegram bot token** — talk to [@BotFather](https://t.me/BotFather)

4. **A DeepSeek API key** — get one at https://platform.deepseek.com/api_keys

---

## Quick Start (Docker)

```bash
# 1. Clone the project
git clone <your-repo-url> safchat && cd safchat

# 2. Create your .env file
cp .env.example .env
nano .env    # paste your TELEGRAM_TOKEN and DEEPSEEK_API_KEY

# 3. Start the bot
docker compose up -d --build

# 4. Watch the logs
docker compose logs -f
```

The bot starts in ~5 seconds. No model to download, no GPU needed.

---

## Configuration (.env)

| Variable              | Required | Default         | Description                                 |
|-----------------------|----------|-----------------|---------------------------------------------|
| `TELEGRAM_TOKEN`      | **Yes**  | (none)          | Bot token from @BotFather                   |
| `DEEPSEEK_API_KEY`    | **Yes**  | (none)          | DeepSeek API key                            |
| `DEEPSEEK_MODEL`      | No       | `deepseek-chat` | DeepSeek model name                         |
| `OLLAMA_HOST`         | No       | localhost:11434 | Ollama URL (only for fallback)              |
| `MODEL_NAME`          | No       | `qwen2.5:0.5b`  | Ollama model (only for fallback)            |
| `DEBUG`               | No       | `false`         | Set to `true` for verbose logs              |

If `DEEPSEEK_API_KEY` is set, the bot uses DeepSeek. Otherwise it tries Ollama.

---

## Useful Commands

| Command                     | What it does                   |
|-----------------------------|--------------------------------|
| `docker compose up -d`      | Start the bot                  |
| `docker compose logs -f`    | Follow logs                    |
| `docker compose down`       | Stop the bot                   |
| `docker compose pull`       | Update the image               |

---

## Bot Commands (in Telegram)

| Command      | Description                     |
|--------------|---------------------------------|
| `/start`     | Set your language (EN / FR)     |
| `/proverb`   | Random Italian proverb          |
| `/tip`       | Learning tip                    |
| `/status`    | Check bot and AI status         |
| `/clear`     | Clear conversation history      |

---

## Running Without Docker (local dev)

```bash
cp .env.example .env
nano .env          # set TELEGRAM_TOKEN + DEEPSEEK_API_KEY
pip install -r requirements.txt
python main.py
```

To use Ollama instead: comment out `DEEPSEEK_API_KEY` in `.env` and
run `ollama serve` separately.

---

## Troubleshooting

**Bot says "TELEGRAM_TOKEN is not set"**
→ Your `.env` is missing the token or still has the placeholder.

**Bot says "DeepSeek API key not configured"**
→ Set your real `DEEPSEEK_API_KEY` in `.env`.

**Bot says "DeepSeek API error"**
→ Check your API key is valid and has credits at
https://platform.deepseek.com/api_keys.

**Permission denied on `/var/run/docker.sock`**
→ Run: `sudo usermod -aG docker $USER && newgrp docker`

---

## Project Structure

```
safchat/
├── main.py               # Entry point — Telegram handlers
├── bot.py                # Command handlers + message routing
├── ai.py                 # AI backends (DeepSeek API + Ollama)
├── config.py             # Environment config + validation
├── proverbs.py           # Proverbs loader and formatter
├── proverbs.json         # Italian proverbs database
├── start.sh              # Local launcher script
├── Dockerfile            # Container image
├── docker-compose.yml    # Single-container setup
├── requirements.txt      # Python dependencies
├── .env.example          # Config template
└── .env                  # Your secrets (git-ignored)
```
