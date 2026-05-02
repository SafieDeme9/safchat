# ai.py - Complete with translation, conversation, and grammar correction
import time
import requests
from config import DEBUG, OLLAMA_HOST, MODEL_NAME

class Ollama:
    def __init__(self):
        self.host = OLLAMA_HOST
        self.model = MODEL_NAME
        self.ready = self._check()
        self.model_ready = self.ready and self._check_model()
        self.conversation_history = {}  # Store conversations per user
        
        if DEBUG:
            if self.ready:
                print(f"✅ Ollama server reachable at {self.host}")
                if self.model_ready:
                    print(f"✅ Model '{self.model}' is available")
                else:
                    print(f"⚠️ Model '{self.model}' not pulled yet - first request may pull it")
            else:
                print(f"⚠️ Ollama not reachable at {self.host}")
    
    def _check(self):
        """Check if Ollama server is reachable"""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def _check_model(self):
        """Check if the specific model is available in Ollama"""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=5)
            if r.status_code == 200:
                models = r.json().get('models', [])
                for m in models:
                    if self.model in m.get('name', ''):
                        return True
            return False
        except:
            return False
    
    def _ensure_model(self):
        """Pull the model if not already available. Returns True if model becomes available."""
        if self.model_ready:
            return True
        try:
            if DEBUG:
                print(f"📥 Pulling model '{self.model}'...")
            r = requests.post(
                f"{self.host}/api/pull",
                json={"name": self.model},
                timeout=300  # 5 min timeout for pulling
            )
            if r.status_code == 200:
                self.model_ready = True
                if DEBUG:
                    print(f"✅ Model '{self.model}' pulled successfully")
                return True
            return False
        except Exception as e:
            if DEBUG:
                print(f"⚠️ Failed to pull model: {e}")
            return False
    
    def chat(self, prompt, system=None, user_id=None):
        """General chat with optional conversation memory"""
        if not self.ready:
            return "⏳ AI server is starting... please wait 60 seconds and try again"
        
        # Try to ensure model is available (non-blocking for first use)
        if not self.model_ready:
            self._ensure_model()
        
        start = time.time()
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        
        # Add conversation history if user_id provided
        if user_id and user_id in self.conversation_history:
            messages.extend(self.conversation_history[user_id][-4:])  # Last 4 exchanges
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            r = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 300}
                },
                timeout=120  # Increased timeout for Pi 4 (CPU inference is slow)
            )
            
            if r.status_code == 404:
                # Model not found - try pulling it
                if self._ensure_model():
                    return self.chat(prompt, system, user_id)  # Retry once
                return "❌ Model not available. The first run downloads the model - please wait 2-3 minutes and try again."
            
            if r.status_code != 200:
                return f"❌ AI error (code {r.status_code})"
            
            response = r.json()['message']['content']
            elapsed = time.time() - start
            
            # Save to conversation history
            if user_id:
                if user_id not in self.conversation_history:
                    self.conversation_history[user_id] = []
                self.conversation_history[user_id].append({"role": "user", "content": prompt})
                self.conversation_history[user_id].append({"role": "assistant", "content": response})
                # Keep only last 10 exchanges to save memory
                if len(self.conversation_history[user_id]) > 20:
                    self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
            
            if DEBUG:
                response += f"\n\n⏱️ ({elapsed:.1f}s)"
            
            return response
            
        except requests.Timeout:
            return "❌ AI is taking too long on Raspberry Pi (try a simpler message or wait for the model to load)"
        except requests.ConnectionError:
            return "❌ Cannot connect to AI server. Is Ollama running?"
        except Exception as e:
            return f"❌ Error: {str(e)[:100]}"
    
    def translate(self, text, source_lang='English'):
        """Translate English or French to Italian"""
        prompt = f"Translate this {source_lang} text to Italian. Only respond with the translation, nothing else.\n\nText: {text}"
        system = "You are a translator. Reply with ONLY the Italian translation, no explanations."
        return self.chat(prompt, system)
    
    def correct_italian(self, text, user_language='en'):
        """Correct Italian grammar and spelling mistakes"""
        prompt = f"""Correct the Italian sentence below. 
Return your response in this exact format:

✅ Corrected: [corrected sentence]
📝 Explanation: [brief explanation of the main error]

Italian sentence to correct: {text}"""
        
        system = "You are an Italian language teacher. Correct grammar and spelling mistakes. Keep explanations short (one sentence)."
        return self.chat(prompt, system)
    
    def converse(self, text, user_language='en', user_id=None):
        """Have a conversation in Italian (tutor mode)"""
        prompt = f"""The user wrote in Italian: "{text}"

Do the following:
1. If there are grammar mistakes, correct them gently
2. Respond naturally in Italian
3. Keep your response to 1-2 sentences
4. Ask a simple follow-up question to continue the conversation"""
        
        system = """You are a friendly Italian tutor. Have a natural conversation in Italian.
Correct mistakes gently. Respond in Italian only.
Keep it simple for learners."""
        
        return self.chat(prompt, system, user_id)
    
    def process_message(self, text, user_language='en', user_id=None):
        """Smart router - decides if user needs translation, correction, or conversation"""
        # Check if user is trying to speak Italian (simple detection)
        italian_words = ['mi piace', 'ciao', 'grazie', 'buongiorno', 'come stai', 'sono', 'ho', 'e']
        is_italian = any(word in text.lower() for word in italian_words)
        
        if is_italian:
            # User is trying Italian - provide correction and conversation
            if DEBUG:
                print(f"🇮🇹 Italian detected - correcting and conversing")
            return self.converse(text, user_language, user_id)
        else:
            # User is speaking English/French - translate
            source = 'English' if user_language == 'en' else 'French'
            if DEBUG:
                print(f"🌐 {source} detected - translating to Italian")
            return self.translate(text, source)