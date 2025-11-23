from serpapi import GoogleSearch

class JobFinder:
    def __init__(self, api_key, max_pages=5, results_per_page=10):
        self.api_key = api_key
        self.max_pages = max_pages
        self.results_per_page = results_per_page
        print("JobFinder instance created.")

    def search_jobs(self, params):
        """
        Executes the job search using SerpApi.
        """
        print(f"Executing search with params: {params}")

        all_res = []

        # Ensure API key is in params
        search_params = params.copy()
        search_params["api_key"] = self.api_key
        
        for page in range(self.max_pages):
            start = page * self.results_per_page
            search_params["start"] = start

            print(f"Searching page {page + 1} with start={start}...")

            search = GoogleSearch(search_params)
            results = search.get_dict()

            if "error" in results:
                print(f"Error from API: {results['error']}")
                break

            page_results = results.get("jobs_results", [])

            print(f"Page {page + 1} returned {len(page_results)} jobs.")

            if not page_results:
                print("No more results found, stopping search.")
                break

            all_res.extend(page_results)
        
        # Debugging: Print what keys are returned
        print(f"DEBUG: Keys returned from API: {list(results.keys())}")
        if "error" in results:
            print(f"DEBUG: API Error: {results['error']}")
        
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

        print(f"Results after dedupe: {len(unique)}")
        return unique


