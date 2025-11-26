import logging
from salary_parser import SalaryParser

class JobParser:
    @staticmethod
    def parse_job(job_data):
        """
        Extracts relevant fields from the raw job data.
        """
        title = job_data.get('title', 'N/A')
        logging.debug(f"Parsing job: {title}")
        company = job_data.get('company_name', 'N/A')
        location = job_data.get('location', 'N/A')
        link = job_data.get('share_link')
        search_location = job_data.get('search_location', 'N/A')
        
        posted_date = "N/A"
        salary_info = None
        salary_raw = "N/A"
        
        if 'extensions' in job_data and job_data['extensions']:
            for item in job_data['extensions']:
                if 'ago' in item or 'day' in item:
                    posted_date = item
                elif SalaryParser.is_salary_text(item):
                    salary_info = SalaryParser.parse_salary(item)
                    salary_raw = item
        
        # Also check detected_extensions if available (SerpApi specific)
        if not salary_info and 'detected_extensions' in job_data:
            exts = job_data['detected_extensions']
            if 'salary' in exts:
                salary_info = SalaryParser.parse_salary(exts['salary'])
                salary_raw = exts['salary']

        min_salary = salary_info[0] if salary_info else None
        max_salary = salary_info[1] if salary_info else None

        return {
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "posted_date": posted_date,
            "search_location": search_location,
            "min_salary": min_salary,
            "max_salary": max_salary,
            "salary_raw": salary_raw
        }