import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        
        # Load search parameters from environment variables with defaults
        self.search_params = {
            "engine": "google_jobs",
            "google_domain": os.getenv("GOOGLE_DOMAIN") or "google.ca",
            "q": os.getenv("SEARCH_QUERY") or "new grad 2026 tech",
            "gl": os.getenv("GL") or "ca",
            "hl": os.getenv("HL") or "en",
            "location": os.getenv("LOCATION") or "Toronto, Ontario, Canada"
        }
