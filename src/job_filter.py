import logging

class JobFilter:
    def __init__(self, config):
        self.blacklist_companies = [c.lower() for c in config.blacklist_companies]
        self.exclude_keywords = [k.lower() for k in config.exclude_keywords]
        self.schedule_types = [s.lower() for s in config.schedule_types]
        self.trusted_domains = [d.lower() for d in config.trusted_domains]

    def is_valid(self, job):
        """
        Checks if a job is valid based on blacklist, keywords, schedule type, and application sources.
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

        # Check application sources
        has_source, source_reason = self.has_reputable_source(job)
        if not has_source:
            return False, source_reason

        return True, None

    def has_reputable_source(self, job):
        """
        Checks if the job has at least one reputable application source.
        Returns (bool, reason).
        """
        apply_options = job.get('apply_options', [])
        if not apply_options:
            # If there are no apply options, we can't determine if it's reputable or not.
            # Assuming we want to filter these out as "low quality" or "not actionable".
            return False, "No application options found"

        company_name = job.get('company_name', '').lower()
        # Normalize company name for URL check (remove spaces, punctuation could be tricky but let's start simple)
        normalized_company = ''.join(e for e in company_name if e.isalnum())
        
        for option in apply_options:
            link = option.get('link', '').lower()
            title = option.get('title', '').lower()
            
            # Check trusted domains
            for domain in self.trusted_domains:
                if domain in link or domain in title:
                    return True, None
            
            # Check direct company page
            # Heuristic: if normalized company name is in the link
            if normalized_company and normalized_company in link:
                return True, None
                    
        return False, "No reputable application source found"
