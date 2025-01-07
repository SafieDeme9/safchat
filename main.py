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

CHOICE = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about what they want to do."""
    reply_keyboard = [["Translation", "Grammar correction", "Conversation"]]

    await update.message.reply_text(
        "Hi! My name is Safchat. I will help you learn italian by holding a conversation with you, translate or correct your grammar. "
        "Send /cancel to stop talking to me.\n\n"
        "What are we going to do?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="translation, grammar correction, conversation"
        ),
    )

    return CHOICE


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()