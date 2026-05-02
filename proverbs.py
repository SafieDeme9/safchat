import json
import random
from pathlib import Path

class Proverbs:
    def __init__(self):
        self.items = []
        self.load()
    
    def load(self):
        try:
            with open('proverbs.json', 'r', encoding='utf-8') as f:
                self.items = json.load(f)['proverbs']
            print(f"✅ Loaded {len(self.items)} proverbs")
        except:
            print("⚠️ No proverbs.json found")
            self.items = []
    
    def random(self, lang='en'):
        if not self.items:
            return "No proverbs available."
        
        p = random.choice(self.items)
        msg = f"📖 *Proverbio Italiano*\n\n🇮🇹 _{p['italian']}_\n\n🇬🇧 {p['english']}"
        
        if lang == 'fr' and 'french' in p:
            msg += f"\n\n🇫🇷 {p['french']}"
        
        msg += f"\n\n💡 _{p['meaning']}_"
        return msg