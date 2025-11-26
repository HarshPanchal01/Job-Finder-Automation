import json
import os
import logging
import hashlib
from datetime import datetime, timedelta

class JobHistory:
    def __init__(self, history_file='data/history.json'):
        self.history_file = history_file
        self.history = {}
        self._ensure_data_dir()
        self.load_history()

    def _ensure_data_dir(self):
        """Ensure the directory for the history file exists."""
        directory = os.path.dirname(self.history_file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def load_history(self):
        """Load history from the JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                logging.info(f"Loaded job history from {self.history_file}")
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Failed to load history file: {e}. Starting with empty history.")
                self.history = {}
        else:
            logging.info("No history file found. Starting with empty history.")
            self.history = {}

    def save_history(self):
        """Save history to the JSON file."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            logging.info(f"Saved job history to {self.history_file}")
        except IOError as e:
            logging.error(f"Failed to save history file: {e}")

    def _generate_id(self, job):
        """Generate a unique ID for a job if one doesn't exist."""
        if 'job_id' in job:
            return job['job_id']
        
        # Fallback: Create a hash from title, company, and location
        unique_string = f"{job.get('title', '')}{job.get('company_name', '')}{job.get('location', '')}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    def is_seen(self, job):
        """Check if a job has been seen before."""
        job_id = self._generate_id(job)
        return job_id in self.history

    def add_job(self, job):
        """Add a job to the history."""
        job_id = self._generate_id(job)
        self.history[job_id] = datetime.now().isoformat()

    def cleanup_old_entries(self, days=90):
        """Remove entries older than the specified number of days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        initial_count = len(self.history)
        
        keys_to_remove = []
        for job_id, timestamp in self.history.items():
            try:
                entry_date = datetime.fromisoformat(timestamp)
                if entry_date < cutoff_date:
                    keys_to_remove.append(job_id)
            except ValueError:
                # If timestamp is invalid, remove it safely or keep it? 
                # Let's remove it to self-heal corruption
                keys_to_remove.append(job_id)
        
        for key in keys_to_remove:
            del self.history[key]
            
        removed_count = initial_count - len(self.history)
        if removed_count > 0:
            logging.info(f"Cleaned up {removed_count} old entries from history.")
            self.save_history()
