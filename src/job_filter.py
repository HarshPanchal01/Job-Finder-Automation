import logging

class JobFilter:
    def __init__(self, config):
        self.blacklist_companies = [c.lower() for c in config.blacklist_companies]
        self.exclude_keywords = [k.lower() for k in config.exclude_keywords]

    def is_valid(self, job):
        """
        Checks if a job is valid based on blacklist and keywords.
        Returns (bool, reason).
        """
        title = job.get('title', '').lower()
        company = job.get('company_name', '').lower()

        # Check company blacklist
        if company in self.blacklist_companies:
            return False, f"Blacklisted company: {job.get('company_name')}"
        
        # Check excluded keywords in title
        for keyword in self.exclude_keywords:
            if keyword in title:
                return False, f"Excluded keyword '{keyword}' in title: {job.get('title')}"

        return True, None
