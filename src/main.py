import logging
from config import Config
from job_finder import JobFinder
from file_manager import FileManager

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

    # Initialize JobFinder
    finder = JobFinder(config.api_key, max_pages=config.max_pages)
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
    
    # Deduplicate aggregated results
    all_jobs = finder.removeDuplicates(all_jobs)
    logging.info(f"Search completed. Total unique jobs found: {len(all_jobs)}")
    
    # Save results
    logging.info("Saving results...")
    FileManager.save_json(all_jobs, 'jobs.json')
    FileManager.save_markdown(all_jobs, 'jobs.md')
    logging.info("Automation completed successfully.")

if __name__ == "__main__":
    main()