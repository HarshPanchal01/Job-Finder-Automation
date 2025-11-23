class JobParser:
    @staticmethod
    def parse_job(job_data):
        """
        Extracts relevant fields from the raw job data.
        """
        title = job_data.get('title', 'N/A')
        print(f"Parsing job: {title}")
        company = job_data.get('company_name', 'N/A')
        location = job_data.get('location', 'N/A')
        link = job_data.get('share_link')
        
        posted_date = "N/A"
        if 'extensions' in job_data and job_data['extensions']:
            for item in job_data['extensions']:
                if 'ago' in item or 'day' in item:
                    posted_date = item
                    break
        
        return {
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "posted_date": posted_date
        }