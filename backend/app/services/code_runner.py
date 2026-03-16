import requests
import time
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class CodeRunner:
    """Judge0 code execution service"""
    
    BASE_URL = "https://judge0-ce.p.rapidapi.com"
    
    LANGUAGE_IDS = {
        'python': 71,
        'cpp': 54,
        'c': 50,
        'javascript': 63,
        'java': 62,
    }
    
    async def run(self, language: str, code: str, input_data: str = "") -> dict:
        """Run code and return result"""
        
        lang_id = self.LANGUAGE_IDS.get(language, 71)
        
        headers = {
            "X-RapidAPI-Key": settings.JUDGE0_API_KEY,
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        
        try:
            # Submit code
            submit_response = requests.post(
                f"{self.BASE_URL}/submissions",
                headers=headers,
                json={
                    "language_id": lang_id,
                    "source_code": code,
                    "stdin": input_data
                }
            )
            
            token = submit_response.json()['token']
            
            # Poll for result
            for _ in range(10):
                result_response = requests.get(
                    f"{self.BASE_URL}/submissions/{token}",
                    headers=headers
                )
                
                data = result_response.json()
                if data['status']['id'] > 2:
                    return {
                        "output": data.get('stdout', '').decode('utf-8') if data.get('stdout') else '',
                        "error": data.get('stderr', '').decode('utf-8') if data.get('stderr') else '',
                        "status": data['status']['description'],
                        "elapsed_time": data.get('time', 0.0)
                    }
                
                time.sleep(0.5)
            
            return {
                "output": "",
                "error": "Timeout",
                "status": "Timeout",
                "elapsed_time": 0.0
            }
        
        except Exception as e:
            logger.error(f"Code run error: {e}")
            raise
    
    async def format_code(self, language: str, code: str) -> str:
        """Format code (placeholder)"""
        return code