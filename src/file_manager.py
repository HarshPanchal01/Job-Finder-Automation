import json
import logging
from job_parser import JobParser

class FileManager:
    @staticmethod
    def save_json(data, filename):
        """
        Saves the raw data to a JSON file.
        """
        logging.info(f"Saving JSON data to {filename}...")
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Job results saved to {filename}")

    @staticmethod
    def save_markdown(jobs, filename):
        """
        Saves the parsed job data to a Markdown file, grouped by search location.
        """
        logging.info(f"Saving Markdown data to {filename}...")
        
        # Group jobs by search_location
        jobs_by_location = {}
        for job in jobs:
            parsed_job = JobParser.parse_job(job)
            # Use 'Unknown Location' if search_location is missing
            loc = parsed_job.get('search_location', 'Unknown Location')
            if loc not in jobs_by_location:
                jobs_by_location[loc] = []
            jobs_by_location[loc].append(parsed_job)
            
        with open(filename, 'w', encoding="utf-8") as f:
            f.write("# Weekly Job Search Results\n\n")
            
            if not jobs:
                f.write("No jobs found this week.\n")
            else:
                for location in sorted(jobs_by_location.keys()):
                    f.write(f"## Jobs in {location}\n\n")
                    for job in jobs_by_location[location]:
                        title = job['title']
                        company = job['company']
                        job_location = job['location']
                        posted_date = job['posted_date']
                        link = job['link']

                        f.write(f"- **{title}** at `{company}` ({job_location})\n")
                        f.write(f"  - **Posted:** {posted_date}\n")
                        if link:
                            f.write(f"  - **Apply:** [Link]({link})\n")
                        f.write("\n")
        
        logging.info(f"Job results summary saved to {filename}")