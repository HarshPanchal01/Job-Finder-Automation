import os
import json
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
        }

        # Handle multiple locations
        locations_str = os.getenv("LOCATIONS")
        if locations_str:
            try:
                # Try parsing as JSON list
                self.locations = json.loads(locations_str)
                # Ensure it's a list
                if not isinstance(self.locations, list):
                    self.locations = [str(self.locations)]
            except json.JSONDecodeError:
                # Fallback: Treat as a single location string
                self.locations = [locations_str]
        else:
            # Default to a single location if LOCATIONS is not set, but treat it as a list
            self.locations = ["Toronto, Ontario, Canada"]
