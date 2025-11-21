from serpapi import GoogleSearch

class JobFinder:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_jobs(self, params):
        """
        Executes the job search using SerpApi.
        """
        # Ensure API key is in params
        search_params = params.copy()
        search_params["api_key"] = self.api_key
        
        search = GoogleSearch(search_params)
        results = search.get_dict()
        return results.get("jobs_results", [])

