import os
import json
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

api_key = os.getenv("API_KEY")

params = {
  "api_key": api_key,
  "engine": "google_jobs",
  "google_domain": "google.ca",
  "q": "new grad 2026 tech",
  "gl": "ca",
  "hl": "en",
  "location": "Toronto, Ontario, Canada"
}

search = GoogleSearch(params)
results = search.get_dict()
jobs_results = results.get("jobs_results", [])

# Save JSON results
with open('jobs.json', 'w') as f:
    json.dump(jobs_results, f, indent=2)

print("Job results saved to jobs.json")

# Create a markdown file for the issue
with open('jobs.md', 'w') as f:
    f.write("## Weekly Job Search Results\n\n")
    if jobs_results:
        for job in jobs_results:
            title = job.get('title', 'N/A')
            company = job.get('company_name', 'N/A')
            location = job.get('location', 'N/A')
            link = job.get('share_link')
            
            posted_date = "N/A"
            if 'extensions' in job and job['extensions']:
                for item in job['extensions']:
                    if 'ago' in item or 'day' in item:
                        posted_date = item
                        break

            f.write(f"- **{title}** at `{company}` ({location})\n")
            f.write(f"  - **Posted:** {posted_date}\n")
            if link:
                f.write(f"  - **Apply:** [Link]({link})\n")
            f.write("\n")
    else:
        f.write("No jobs found this week.\n")

print("Job results summary saved to jobs.md")
