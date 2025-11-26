import logging
from config import Config
from job_finder import JobFinder
from file_manager import FileManager
from job_history import JobHistory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def main():
    logging.info("Starting Job Finder Automation...")
    # Initialize configuration
    config = Config()
    logging.info("Configuration loaded.")
    
    if not config.api_key:
        logging.error("API_KEY not found in environment variables.")
        return

    # Initialize JobFinder and JobHistory
    finder = JobFinder(config.api_key, max_pages=config.max_pages)
    history = JobHistory()
    logging.info(f"JobFinder initialized with max_pages={config.max_pages}.")
    
    all_jobs = []
    
    for location in config.locations:
        logging.info(f"Searching for jobs in {location}...")
        # Execute search
        search_params = config.search_params.copy()
        search_params["location"] = location
        
        jobs = finder.search_jobs(search_params)
        logging.info(f"Found {len(jobs)} jobs in {location}.")
        all_jobs.extend(jobs)
    
    # Deduplicate aggregated results (intra-run duplicates)
    all_jobs = finder.removeDuplicates(all_jobs)
    logging.info(f"Total unique jobs found in this run: {len(all_jobs)}")

    # Filter out jobs seen in previous runs (inter-run duplicates)
    new_jobs = []
    for job in all_jobs:
        if not history.is_seen(job):
            new_jobs.append(job)
            history.add_job(job)
    
    logging.info(f"Net new jobs after history check: {len(new_jobs)}")
    
    # Save results
    logging.info("Saving results...")
    FileManager.save_json(new_jobs, 'jobs.json')
    FileManager.save_markdown(new_jobs, 'jobs.md')
    
    # Save history and cleanup
    history.save_history()
    history.cleanup_old_entries()
    
    logging.info("Automation completed successfully.")

if __name__ == "__main__":
    main()