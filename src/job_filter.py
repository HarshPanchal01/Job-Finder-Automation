import logging

class JobFilter:
    def __init__(self, config):
        self.blacklist_companies = [c.lower() for c in config.blacklist_companies]
        self.exclude_keywords = [k.lower() for k in config.exclude_keywords]
        self.schedule_types = [s.lower() for s in config.schedule_types]

    def is_valid(self, job):
        """
        Checks if a job is valid based on blacklist, keywords, and schedule type.
        Returns (bool, reason).
        """
        title = job.get('title', '').lower()
        company = job.get('company_name', '').lower()
        schedule_type = job.get('detected_extensions', {}).get('schedule_type', '').lower()

        # Check company blacklist
        if company in self.blacklist_companies:
            return False, f"Blacklisted company: {job.get('company_name')}"
        
        # Check excluded keywords in title
        for keyword in self.exclude_keywords:
            if keyword in title:
                return False, f"Excluded keyword '{keyword}' in title: {job.get('title')}"

        # Check schedule type
        if schedule_type:
            # Check if any allowed schedule type is present in the job's schedule type string
            is_allowed = False
            for allowed_type in self.schedule_types:
                if allowed_type in schedule_type:
                    is_allowed = True
                    break
            
            if not is_allowed:
                return False, f"Invalid schedule type: {job.get('detected_extensions', {}).get('schedule_type')}"

        return True, None
