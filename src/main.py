from config import Config
from job_finder import JobFinder
from file_manager import FileManager

def main():
    # Initialize configuration
    config = Config()
    
    if not config.api_key:
        print("Error: API_KEY not found in environment variables.")
        return

    # Initialize JobFinder
    finder = JobFinder(config.api_key)
    
    print("Searching for jobs...")
    # Execute search
    jobs = finder.search_jobs(config.search_params)
    
    # Save results
    FileManager.save_json(jobs, 'jobs.json')
    FileManager.save_markdown(jobs, 'jobs.md')

if __name__ == "__main__":
    main()
