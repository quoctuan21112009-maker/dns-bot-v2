from groq import Groq
from openai import OpenAI
from typing import Tuple
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    """AI Service supporting multiple providers"""
    
    def __init__(self, provider: str = "groq", api_key: str = ""):
        self.provider = provider.lower()
        self.api_key = api_key or settings.GROQ_API_KEY
        
        if self.provider == "groq":
            self.client = Groq(api_key=self.api_key)
        elif self.provider == "openai":
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = Groq(api_key=self.api_key)
    
    async def chat(self, message: str, model: str = None) -> Tuple[str, int]:
        """Chat with AI"""
        
        if model is None:
            model = settings.DEFAULT_AI_MODEL
        
        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Bạn là DNS Bot - AI Assistant cho lớp 11A1"
                        },
                        {"role": "user", "content": message}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
            else:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": message}],
                    temperature=0.7
                )
            
            reply = response.choices[0].message.content
            tokens = response.usage.total_tokens
            
            return reply, tokens
        
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            raise