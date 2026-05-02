# bot.py - Complete with clear command
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import DEBUG
from proverbs import Proverbs
from ai import Ollama

# Learning tips
TIPS = {
    'en': [
        "💡 Practice 15 minutes daily - consistency wins!",
        "💡 Watch Italian YouTube with subtitles",
        "💡 Italian is phonetic - say every letter clearly",
        "💡 Learn the 100 most common words first",
        "💡 Listen to Italian music while driving",
        "💡 Try to think in Italian, not translate",
        "💡 Keep a notebook of new words",
        "💡 Find an Italian conversation partner",
    ],
    'fr': [
        "💡 Pratiquez 15 minutes par jour - la clé!",
        "💡 Regardez YouTube en italien sous-titré",
        "💡 L'italien est phonétique - prononcez tout",
        "💡 Apprenez d'abord les 100 mots courants",
        "💡 Écoutez de la musique italienne",
        "💡 Essayez de penser en italien",
        "💡 Tenez un carnet de nouveaux mots",
        "💡 Trouvez un partenaire de conversation italien",
    ]
}

class ItalianBot:
    def __init__(self):
        self.proverbs = Proverbs()
        self.ai = Ollama()
        self.user_lang = {}
        
        if DEBUG:
            print("🤖 Bot initialized")
            print(f"   Proverbs: {len(self.proverbs.items)} loaded")
            print(f"   AI ready: {self.ai.ready}")
    
    async def start(self, update, context):
        keyboard = [[
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr')
        ]]
        
        status = "✅ AI ready" if self.ai.ready and self.ai.model_ready else "⏳ First request loads model (may take 2-3 min)..."
        
        await update.message.reply_text(
            f"Ciao!{update.effective_user.first_name} 👋\n\n"
            f"🇮🇹 *I'am Safchat Italian Tutor Bot*\n"
            f"{status}\n\n"
            f"I can:\n"
            f"• 📝 Correct your Italian grammar\n"
            f"• 💬 Have conversations in Italian\n"
            f"• 🌐 Translate EN/FR → Italian\n"
            f"• 📖 Send Italian proverbs (/proverb)\n"
            f"• 💡 Give learning tips (/tip)\n\n"
            f"Choose your language:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def language_callback(self, update, context):
        query = update.callback_query
        await query.answer()
        
        lang = query.data.split('_')[1]
        user_id = query.from_user.id
        self.user_lang[user_id] = lang
        
        if lang == 'en':
            msg = "🇬🇧 Great! Send me:\n"
            msg += "• English text → I'll translate to Italian\n"
            msg += "• Italian text → I'll correct you and reply in Italian\n\n"
            msg += "Commands:\n/proverb - Random proverb\n/tip - Learning tip\n/status - Check AI\n/clear - Clear conversation"
        else:
            msg = "🇫🇷 Super! Envoyez-moi:\n"
            msg += "• Texte français → Je traduis en italien\n"
            msg += "• Texte italien → Je corrige et réponds en italien\n\n"
            msg += "Commandes:\n/proverb - Proverbe\n/tip - Conseil\n/status - État AI\n/clear - Effacer conversation"
        
        await query.edit_message_text(msg)
    
    async def proverb(self, update, context):
        user_id = update.effective_user.id
        lang = self.user_lang.get(user_id, 'en')
        proverb_text = self.proverbs.random(lang)
        await update.message.reply_text(proverb_text, parse_mode='Markdown')
    
    async def tip(self, update, context):
        user_id = update.effective_user.id
        lang = self.user_lang.get(user_id, 'en')
        tip = random.choice(TIPS.get(lang, TIPS['en']))
        await update.message.reply_text(tip, parse_mode='Markdown')
    
    async def status(self, update, context):
        status_text = f"🤖 *Bot Status*\n\n"
        status_text += f"✅ Bot running\n"
        status_text += f"📚 Proverbs: {len(self.proverbs.items)}\n"
        status_text += f"🧠 Ollama: {'✅ Online' if self.ai.ready else '❌ Offline'}\n"
        status_text += f"📦 Model: {self.ai.model}\n"
        status_text += f"📥 Model loaded: {'✅ Yes' if self.ai.model_ready else '⏳ Loading'}\n"
        
        user_id = update.effective_user.id
        if user_id in self.ai.conversation_history:
            history_len = len(self.ai.conversation_history[user_id])
            status_text += f"💬 Your history: {history_len} messages\n"
        
        if DEBUG:
            status_text += f"\n🔧 Debug mode: ON"
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    # ✅ ADD THIS METHOD - The one you're missing!
    async def clear(self, update, context):
        """Clear conversation history for the user"""
        user_id = update.effective_user.id
        if user_id in self.ai.conversation_history:
            self.ai.conversation_history[user_id] = []
            msg = "🗑️ Conversation history cleared!"
        else:
            msg = "No conversation history to clear."
        
        await update.message.reply_text(msg)
    
    async def handle_message(self, update, context):
        user_id = update.effective_user.id
        
        # First time user? Ask for language
        if user_id not in self.user_lang:
            await self.start(update, context)
            return
        
        user_language = self.user_lang[user_id]
        text = update.message.text
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        
        if DEBUG:
            print(f"📨 [{user_id}] {text[:50]}")
        
        # Process message with AI (detects Italian vs EN/FR automatically)
        response = self.ai.process_message(text, user_language, user_id)
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def error(self, update, context):
        print(f"❌ Error: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Something went wrong. Please try again."
            )