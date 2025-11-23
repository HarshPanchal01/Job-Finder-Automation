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
        with open(filename, 'w', encoding="utf-8") as f:
            f.write("## Weekly Job Search Results\n\n")
            if jobs:
                for job in jobs:
                    parsed_job = JobParser.parse_job(job)
                    
                    title = parsed_job['title']
                    company = parsed_job['company']
                    location = parsed_job['location']
                    posted_date = parsed_job['posted_date']
                    link = parsed_job['link']

                    f.write(f"- **{title}** at `{company}` ({location})\n")
                    f.write(f"  - **Posted:** {posted_date}\n")
                    if link:
                        f.write(f"  - **Apply:** [Link]({link})\n")
                    f.write("\n")
            else:
                f.write("No jobs found this week.\n")
        
        print(f"Job results summary saved to {filename}")