from serpapi import GoogleSearch

class JobFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        print("JobFinder instance created.")

    def search_jobs(self, params):
        """
        Executes the job search using SerpApi.
        """
        print(f"Executing search with params: {params}")
        # Ensure API key is in params
        search_params = params.copy()
        search_params["api_key"] = self.api_key
        
        search = GoogleSearch(search_params)
        results = search.get_dict()
        
        # Debugging: Print what keys are returned
        print(f"DEBUG: Keys returned from API: {list(results.keys())}")
        if "error" in results:
            print(f"DEBUG: API Error: {results['error']}")
        
        return results.get("jobs_results", [])

