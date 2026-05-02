import os
from dotenv import load_dotenv

load_dotenv()

# Set to False on Raspberry Pi for production
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'bot_token')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
# Use an ultra-lightweight model suitable for Raspberry Pi 4 (4GB RAM)
# qwen2.5:0.5b = 0.5B params, ~400MB download, ~500-600MB RAM at inference
MODEL_NAME = os.getenv('MODEL_NAME', 'qwen2.5:0.5b')
