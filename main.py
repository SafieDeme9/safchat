import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("bot_token")
if not TOKEN:
    raise ValueError("The bot token is not defined.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the conversation and asks the user about what they want to do."""

    await update.message.reply_text(
        "Hi! My name is Safchat I am an LLM powered chatbot. I will help you learn italian by holding a conversation with you or translate. \n"
        "Send /translate to translate in italian, /chat to hold a conversation with the bot and /help to get a help.\n"
        "Send /cancel to stop talking to me.\n\n"
        "What are we going to do?"
    )
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Give the user the commands"""

    await update.message.reply_text(
        "Send /translate to translate in italian, /chat to hold a conversation with the bot and /help to get a help.\n"
        "Send /cancel to stop talking to me.\n\n"
        "What are we going to do?"
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler("help", help))

    
    application.run_polling()