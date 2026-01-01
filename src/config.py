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

        # Handle multiple queries
        queries_str = os.getenv("SEARCH_QUERIES")
        if queries_str:
            self.queries = self._parse_list(queries_str)
        else:
            # Default if SEARCH_QUERIES is not set
            self.queries = ["software developer"]

        # Pagination settings
        try:
            self.max_pages = int(os.getenv("MAX_PAGES") or 5)
        except ValueError:
            self.max_pages = 5

        # Salary filtering
        try:
            self.min_salary = int(os.getenv("MIN_SALARY") or 0)
        except ValueError:
            self.min_salary = 0

        # Date filtering
        try:
            self.max_days_old = int(os.getenv("MAX_DAYS_OLD") or 7)
        except ValueError:
            self.max_days_old = 7

        # Blacklist and Keywords
        self.blacklist_companies = self._parse_list(os.getenv("BLACKLIST_COMPANIES"))
        self.exclude_keywords = self._parse_list(os.getenv("EXCLUDE_KEYWORDS"))

        # Schedule Types
        schedule_types_str = os.getenv("SCHEDULE_TYPES")
        if schedule_types_str:
            self.schedule_types = self._parse_list(schedule_types_str)
        else:
            # Default to Full-time if not specified
            self.schedule_types = ["full-time"]

        # Trusted Domains for Application Sources
        trusted_domains_str = os.getenv("TRUSTED_DOMAINS")
        if trusted_domains_str:
            self.trusted_domains = self._parse_list(trusted_domains_str)
        else:
            # Default trusted domains
            self.trusted_domains = ["linkedin", "glassdoor", "indeed", "ziprecruiter", "simplyhired"]

        # Email Configuration
        self.smtp_server = os.getenv("SMTP_SERVER") or "smtp.gmail.com"
        try:
            self.smtp_port = int(os.getenv("SMTP_PORT") or 587)
        except ValueError:
            self.smtp_port = 587
            
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        
        # Handle multiple receivers
        receivers_str = os.getenv("EMAIL_RECEIVER")
        if receivers_str:
            self.email_receivers = self._parse_list(receivers_str)
        elif self.email_address:
            self.email_receivers = [self.email_address]
        else:
            self.email_receivers = []

    def _parse_list(self, env_str):
        """Parses a JSON list string or comma-separated string into a list."""
        if not env_str:
            return []
        try:
            parsed = json.loads(env_str)
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
            return [str(parsed)]
        except json.JSONDecodeError:
            # Fallback: comma-separated
            return [item.strip() for item in env_str.split(',') if item.strip()]