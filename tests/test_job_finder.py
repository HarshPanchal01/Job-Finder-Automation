import pytest
import logging
import json
from unittest.mock import MagicMock, patch
from job_finder import JobFinder

@pytest.fixture
def job_finder():
    return JobFinder(api_key="test_key", max_pages=2)

@pytest.fixture
def job_finder_with_retries():
    return JobFinder(api_key="test_key", max_pages=2, max_retries=3)

def test_search_jobs_success(job_finder):
    """Test successful job search with pagination."""
    logging.info("Testing search_jobs success scenario...")
    mock_results_page_1 = {
        "jobs_results": [{"title": "Job 1"}],
        "serpapi_pagination": {"next_page_token": "token_123"}
    }
    mock_results_page_2 = {
        "jobs_results": [{"title": "Job 2"}],
        # No next page token
    }

    with patch("job_finder.GoogleSearch") as MockSearch:
        # Setup mock to return different results for each call
        mock_instance = MockSearch.return_value
        mock_instance.get_dict.side_effect = [mock_results_page_1, mock_results_page_2]

        params = {"q": "test"}
        results = job_finder.search_jobs(params)

        assert len(results) == 2
        assert results[0]["title"] == "Job 1"
        assert results[1]["title"] == "Job 2"
        assert MockSearch.call_count == 2
    logging.info("search_jobs success test passed.")

def test_search_jobs_api_error(job_finder):
    """Test handling of API errors."""
    logging.info("Testing search_jobs API error handling...")
    mock_results = {"error": "Invalid API key"}

    with patch("job_finder.GoogleSearch") as MockSearch:
        mock_instance = MockSearch.return_value
        mock_instance.get_dict.return_value = mock_results

        params = {"q": "test"}
        results = job_finder.search_jobs(params)

        assert len(results) == 0
    logging.info("search_jobs API error test passed.")

def test_search_jobs_location_injection(job_finder):
    """Test that search_location is injected into results."""
    logging.info("Testing search_jobs location injection...")
    mock_results = {
        "jobs_results": [{"title": "Job 1"}]
    }

    with patch("job_finder.GoogleSearch") as MockSearch:
        mock_instance = MockSearch.return_value
        mock_instance.get_dict.return_value = mock_results

        params = {"q": "test", "location": "New York"}
        results = job_finder.search_jobs(params)

        assert results[0]["search_location"] == "New York"
    logging.info("search_jobs location injection test passed.")

def test_remove_duplicates(job_finder):
    """Test duplicate removal logic."""
    logging.info("Testing remove_duplicates...")
    jobs = [
        {"title": "Dev", "company": "A", "location": "NY"},
        {"title": "Dev", "company": "A", "location": "NY"}, # Duplicate
        {"title": "Dev", "company": "B", "location": "NY"}, # Different company
    ]
    
    unique_jobs = job_finder.removeDuplicates(jobs)
    
    assert len(unique_jobs) == 2
    assert unique_jobs[0]["company"] == "A"
    assert unique_jobs[1]["company"] == "B"
    logging.info("remove_duplicates test passed.")

def test_fetch_with_retry_success_after_failure(job_finder_with_retries):
    """Test that retry logic recovers from transient JSON errors."""
    logging.info("Testing retry logic with recovery...")
    mock_results = {"jobs_results": [{"title": "Job 1"}]}

    with patch("job_finder.GoogleSearch") as MockSearch, \
         patch("job_finder.time.sleep") as mock_sleep:
        mock_instance = MockSearch.return_value
        # First call raises JSONDecodeError, second succeeds
        mock_instance.get_dict.side_effect = [
            json.JSONDecodeError("Expecting value", "", 0),
            mock_results
        ]

        params = {"q": "test"}
        results = job_finder_with_retries.search_jobs(params)

        assert len(results) == 1
        assert results[0]["title"] == "Job 1"
        assert mock_instance.get_dict.call_count == 2
        mock_sleep.assert_called_once_with(1)  # 2^0 = 1 second backoff
    logging.info("Retry recovery test passed.")

def test_fetch_with_retry_max_retries_exceeded(job_finder_with_retries):
    """Test that max retries raises exception."""
    logging.info("Testing max retries exceeded...")

    with patch("job_finder.GoogleSearch") as MockSearch, \
         patch("job_finder.time.sleep"):
        mock_instance = MockSearch.return_value
        # All calls raise JSONDecodeError
        mock_instance.get_dict.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        params = {"q": "test"}
        with pytest.raises(json.JSONDecodeError):
            job_finder_with_retries.search_jobs(params)

        assert mock_instance.get_dict.call_count == 3  # max_retries = 3
    logging.info("Max retries test passed.")

def test_fetch_with_retry_exponential_backoff(job_finder_with_retries):
    """Test that exponential backoff timing is correct."""
    logging.info("Testing exponential backoff timing...")

    with patch("job_finder.GoogleSearch") as MockSearch, \
         patch("job_finder.time.sleep") as mock_sleep:
        mock_instance = MockSearch.return_value
        mock_results = {"jobs_results": [{"title": "Job 1"}]}
        # Fail twice, succeed on third
        mock_instance.get_dict.side_effect = [
            json.JSONDecodeError("Expecting value", "", 0),
            json.JSONDecodeError("Expecting value", "", 0),
            mock_results
        ]

        params = {"q": "test"}
        results = job_finder_with_retries.search_jobs(params)

        assert len(results) == 1
        # Check exponential backoff: 2^0=1, 2^1=2
        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1)
        mock_sleep.assert_any_call(2)
    logging.info("Exponential backoff test passed.")