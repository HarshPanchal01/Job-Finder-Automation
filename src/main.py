from config import Config
from job_finder import JobFinder
from file_manager import FileManager

def main():
    print("Starting Job Finder Automation...")
    # Initialize configuration
    config = Config()
    print("Configuration loaded.")
    
    if not config.api_key:
        print("Error: API_KEY not found in environment variables.")
        return

    # Initialize JobFinder
    finder = JobFinder(config.api_key, max_pages=config.max_pages)
    print(f"JobFinder initialized with max_pages={config.max_pages}.")
    
    all_jobs = []
    
    for location in config.locations:
        print(f"Searching for jobs in {location}...")
        # Execute search
        search_params = config.search_params.copy()
        search_params["location"] = location
        
        jobs = finder.search_jobs(search_params)
        print(f"Found {len(jobs)} jobs in {location}.")
        all_jobs.extend(jobs)
    
    # Deduplicate aggregated results
    all_jobs = finder.removeDuplicates(all_jobs)
    print(f"Search completed. Total unique jobs found: {len(all_jobs)}")
    
    # Save results
    print("Saving results...")
    FileManager.save_json(all_jobs, 'jobs.json')
    FileManager.save_markdown(all_jobs, 'jobs.md')
    print("Automation completed successfully.")

if __name__ == "__main__":
    main()