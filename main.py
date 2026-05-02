#!/usr/bin/env python3
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config import TELEGRAM_TOKEN, DEBUG
from bot import ItalianBot

def main():
    bot = ItalianBot()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("proverb", bot.proverb))
    app.add_handler(CommandHandler("tip", bot.tip))
    app.add_handler(CommandHandler("status", bot.status))
    app.add_handler(CallbackQueryHandler(bot.language_callback, pattern='^lang_'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))   
    app.add_error_handler(bot.error)
    app.add_handler(CommandHandler("clear", bot.clear))
    
    print("🤖 Italian Bot is running...")
    print(f"   Mode: {'DEBUG' if DEBUG else 'PRODUCTION'}")
    print("   Press Ctrl+C to stop")
    app.run_polling()

if __name__ == '__main__':
    main()