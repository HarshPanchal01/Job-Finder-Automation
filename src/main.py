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
    finder = JobFinder(config.api_key)
    print("JobFinder initialized.")
    
    print("Searching for jobs...")
    # Execute search
    jobs = finder.search_jobs(config.search_params)
    jobs = finder.removeDuplicates(jobs)
    print(f"Search completed. Found {len(jobs)} jobs.")
    
    # Save results
    print("Saving results...")
    FileManager.save_json(jobs, 'jobs.json')
    FileManager.save_markdown(jobs, 'jobs.md')
    print("Automation completed successfully.")

if __name__ == "__main__":
    main()