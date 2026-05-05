# Safchat — AI Italian Tutor Telegram Bot

A Telegram bot that helps you learn Italian using a self-hosted Ollama LLM
(`qwen2.5:0.5b`, ~400 MB — ideal for Raspberry Pi 4).

**What it does:**
- Translates English / French to Italian
- Corrects your Italian grammar and spelling
- Has simple conversations in Italian
- Sends random Italian proverbs (`/proverb`)
- Gives learning tips (`/tip`)

---

## Prerequisites (Raspberry Pi 4)

1. **Docker** and **Docker Compose** installed:
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo apt install docker-compose-plugin -y
   ```

2. **Add your user to the `docker` group** (so you don't need `sudo`):
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```
   > If you skip this step, you'll get `PermissionError: Permission denied` when
   > trying to connect to `/var/run/docker.sock`.

3. **A Telegram bot token** — talk to [@BotFather](https://t.me/BotFather) on
   Telegram, create a new bot, and copy the token.

---

## Quick Start (Docker)

```bash
# 1. Clone the project
git clone <your-repo-url> safchat && cd safchat

# 2. Create your .env file
cp .env.example .env

# 3. Edit .env — paste your real TELEGRAM_TOKEN
nano .env

# 4. Start everything (Ollama + bot)
docker compose up -d --build

# 5. Check logs (first run pulls the model — be patient, ~2-5 min on RPi 4)
docker compose logs -f
```

Once you see `🤖 Italian Bot is running...` the bot is online. Open Telegram and
send `/start` to your bot.

---

## Configuration (.env)

| Variable         | Required | Default               | Description                                |
|------------------|----------|-----------------------|--------------------------------------------|
| `TELEGRAM_TOKEN` | **Yes**  | (none)                | Bot token from @BotFather                  |
| `OLLAMA_HOST`    | No       | `http://localhost:11434` | Ollama API URL (Docker overrides this) |
| `MODEL_NAME`     | No       | `qwen2.5:0.5b`        | Ollama model to use                        |
| `DEBUG`          | No       | `false`               | Set to `true` for verbose logs             |

When using Docker, `OLLAMA_HOST` is automatically set to `http://ollama:11434`
inside the container — you do **not** need to change it in `.env`.

---

## Running Without Docker (local dev)

```bash
# You need Ollama running separately
ollama serve         # in one terminal
ollama pull qwen2.5:0.5b

# Then:
cp .env.example .env
nano .env            # set OLLAMA_HOST=http://localhost:11434 + your token
pip install -r requirements.txt
python main.py
```

---

## Useful Commands

| Command                 | What it does                       |
|-------------------------|------------------------------------|
| `docker compose up -d`  | Start in background                |
| `docker compose logs -f`| Follow logs (Ctrl+C to stop)       |
| `docker compose down`   | Stop and remove containers         |
| `docker compose restart`| Restart containers                 |
| `docker compose pull`   | Update images                      |

---

## Troubleshooting

**Bot says "TELEGRAM_TOKEN is not set"**
→ Make sure `.env` exists and contains `TELEGRAM_TOKEN=your_real_token`
(not the placeholder `YOUR_TELEGRAM_BOT_TOKEN_HERE`).

**Bot can't connect to Ollama (❌ Cannot connect to AI server)**
→ Wait 2-5 minutes on first run — the model is downloading. Check with
`docker compose logs ollama`.

**Permission denied on `/var/run/docker.sock`**
→ Your user is not in the `docker` group. Run:
```bash
sudo usermod -aG docker $USER && newgrp docker
```

**Raspberry Pi runs out of memory**
→ The Ollama container is limited to 3.5 GB RAM and 3 CPUs in
`docker-compose.yml` — adjust `mem_limit` and `cpus` to match your Pi.

---

## Project Structure

```
safchat/
├── main.py               # Entry point — sets up Telegram handlers
├── bot.py                # Command handlers and message routing
├── ai.py                 # Ollama API client (chat, translate, correct)
├── config.py             # Environment variable loading + validation
├── proverbs.py           # Proverbs loader and formatter
├── proverbs.json         # Italian proverbs database
├── start.sh              # Launcher for non-Docker runs
├── ollama-entrypoint.sh  # Ollama container entrypoint (pulls model)
├── Dockerfile            # Bot container image
├── docker-compose.yml    # Multi-container setup (Ollama + Bot)
├── requirements.txt      # Python dependencies
├── .env.example          # Template for your .env file
└── .env                  # Your secrets (git-ignored)
```
