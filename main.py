import os
import logging
from dotenv import load_dotenv
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler # type: ignore
from transformers import pipeline
import random
from pathlib import Path

def get_random_proverb_formatted():
    """Return a formatted string of a random proverb for Telegram."""
    json_path = Path(__file__).parent / "proverbs.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    proverb = random.choice(data["proverbs"])
    
    # Format for Italian learners
    message = f"📖 *Italian Proverb*\n\n"
    message += f"🇮🇹 _{proverb['italian']}_\n\n"
    message += f"🇬🇧 {proverb['english']}\n\n"
    message += f"💡 _{proverb['meaning']}_"
    
    return message

# Usage in your bot:
# random_proverb = get_random_proverb_formatted()
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("bot_token")
if not TOKEN:
    raise ValueError("The bot token is not defined.")

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-it")

def get_random_proverb():
    pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the conversation and asks the user about what they want to do."""

    await update.message.reply_text(
        "Hi! My name is Safchat I am an LLM powered chatbot. I will help you learn italian by holding a conversation with you or translate. \n"
        "Send /translate + text to translate from english to italian,\n" 
        "/chat to hold a conversation with the bot and\n"
        "/help to get a help.\n"
        "/proverb to get a random italian proverb.\n"
        "Send /cancel to stop talking to me.\n\n"
        "What are we going to do?"
    )
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explains to the user the commands"""

    await update.message.reply_text(
        "Send /translate to translate in italian, /chat to hold a conversation with the bot and /help to get a help.\n"
        "Send /cancel to stop talking to me.\n\n"
        "What are we going to do?"
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Good bye and thanks for using Safchat!"
    )

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Translate English text to Italian."""
    if context.args:
        input_text = " ".join(context.args)
        try:
            translated = translator(input_text)
            translated_text = translated[0]['translation_text']
            await update.message.reply_text(f"Translated text: {translated_text}")
        except Exception as e:
            await update.message.reply_text(f"An error occurred during translation: {e}")
    else:
        await update.message.reply_text("Please provide the text to translate. Example:\n/translate Hello, how are you?")
async def proverb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random Italian proverb."""
    proverb = get_random_proverb_formatted()
    await update.message.reply_text(proverb, parse_mode="Markdown")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("translate", translate))
    application.add_handler(CommandHandler("proverb", proverb))
    
    application.run_polling()