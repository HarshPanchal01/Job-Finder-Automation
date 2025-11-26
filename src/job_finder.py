import logging
from serpapi import GoogleSearch

class JobFinder:
    def __init__(self, api_key, max_pages=5, results_per_page=10):
        self.api_key = api_key
        self.max_pages = max_pages
        self.results_per_page = results_per_page
        self.total_api_calls = 0
        logging.info("JobFinder instance created.")

    def search_jobs(self, params):
        """
        Executes the job search using SerpApi.
        """
        logging.info(f"Executing search with params: {params}")

        all_res = []
        next_page_token = None

        # Ensure API key is in params
        search_params = params.copy()
        search_params["api_key"] = self.api_key
        
        for page in range(self.max_pages):
            if next_page_token:
                search_params["next_page_token"] = next_page_token
                logging.info(f"Fetching next page with token.")
            else:
                logging.info("Fetching first page of results.")

            search = GoogleSearch(search_params)
            logging.info("Sending request to SerpApi...")
            results = search.get_dict()
            self.total_api_calls += 1

            if "error" in results:
                logging.error(f"Error from API: {results['error']}")
                break

            page_results = results.get("jobs_results", [])

            logging.info(f"Page {page + 1} returned {len(page_results)} jobs.")

            if not page_results:
                logging.info("No more results found, stopping search.")
                break

            all_res.extend(page_results)

            next_page_token = results.get("serpapi_pagination", {}).get("next_page_token")

            if not next_page_token:
                logging.info("No next page token found, ending pagination.")
                break
        
        # Debugging: Print what keys are returned
        logging.debug(f"DEBUG: Keys returned from API: {list(results.keys())}")
        if "error" in results:
            logging.debug(f"DEBUG: API Error: {results['error']}")
        
        # Inject search location into each job result
        search_location = params.get("location", "Unknown")
        for job in all_res:
            job["search_location"] = search_location

        return all_res
    
    def removeDuplicates(self, jobs):
        """
        Removes duplicate jobs based on (title, company, location).
        """
        seen = set()
        unique = []

        for job in jobs:
            key = (
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", "")
            )
            if key not in seen:
                seen.add(key)
                unique.append(job)

        # Calculate duplicates as the difference between the original
        # number of jobs and the number of unique jobs found.
        duplicates = len(jobs) - len(unique)
        logging.info(f"{duplicates} duplicates found.")
        logging.info(f"Results after removing duplicates: {len(unique)}")
        return unique