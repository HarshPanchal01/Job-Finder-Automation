import json
from job_parser import JobParser

class FileManager:
    @staticmethod
    def save_json(data, filename):
        """
        Saves the raw data to a JSON file.
        """
        print(f"Saving JSON data to {filename}...")
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Job results saved to {filename}")

    @staticmethod
    def save_markdown(jobs, filename):
        """
        Saves the parsed job data to a Markdown file.
        """
        print(f"Saving Markdown data to {filename}...")
        
        # Group jobs by search location
        jobs_by_location = {}
        for job in jobs:
            parsed_job = JobParser.parse_job(job)
            search_loc = parsed_job.get('search_location', 'Unknown Location')
            if search_loc not in jobs_by_location:
                jobs_by_location[search_loc] = []
            jobs_by_location[search_loc].append(parsed_job)

        with open(filename, 'w') as f:
            f.write("## Weekly Job Search Results\n\n")
            
            if not jobs:
                f.write("No jobs found this week.\n")
            else:
                for location, location_jobs in jobs_by_location.items():
                    f.write(f"### Jobs in {location}\n\n")
                    for job in location_jobs:
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
        
        print(f"Job results summary saved to {filename}")
