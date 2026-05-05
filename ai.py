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
    
    def process_message(self, text, user_language='en', user_id=None):
        """Let the model decide: translate if EN/FR, correct+converse if Italian"""
        native = 'English' if user_language == 'en' else 'French'

        system = (
            "You are a friendly Italian language tutor. "
            "If the user writes in English or French, translate their message to Italian. "
            "If the user writes in Italian, correct any grammar mistakes gently "
            "and reply naturally in Italian (1-2 sentences, ask a follow-up question). "
            "Always respond in Italian only. Keep corrections brief and encouraging."
        )

        user_msg = f"[The user's native language is {native}]\n\n{text}"

        if DEBUG:
            print(f"📨 [{user_id}] {text[:80]}")

        return self.chat(user_msg, system, user_id)