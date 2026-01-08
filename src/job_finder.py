import logging
import time
import json
from serpapi import GoogleSearch

class JobFinder:
    def __init__(self, api_key, max_pages=5, max_retries=3):
        self.api_key = api_key
        self.max_pages = max_pages
        self.total_api_calls = 0
        self.max_retries = max_retries
        logging.info("JobFinder instance created.")

    def _fetch_with_retry(self, search_params) -> dict:
        """
        Fetches results from SerpApi with retry logic for transient failures.
        """
        for attempt in range(self.max_retries):
            try:
                search = GoogleSearch(search_params)
                logging.info("Sending request to SerpApi...")
                results = search.get_dict()
                self.total_api_calls += 1
                return results
            except json.JSONDecodeError as e:
                logging.warning(f"API returned invalid JSON (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error("Max retries reached. API request failed.")
                    raise
            except Exception as e:
                logging.warning(f"API request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    logging.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logging.error("Max retries reached. API request failed.")
                    raise
        # This should never be reached due to raise statements above
        raise RuntimeError("Failed to fetch results after all retries")

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

            results = self._fetch_with_retry(search_params)

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