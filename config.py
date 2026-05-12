import os
import sys
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', os.getenv('OLLAMA_MODEL', 'qwen2.5:0.5b'))

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_MODEL = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN_HERE':
    print("❌ ERROR: TELEGRAM_TOKEN is not set!")
    print("   Copy .env.example to .env and add your bot token from @BotFather")
    sys.exit(1)
