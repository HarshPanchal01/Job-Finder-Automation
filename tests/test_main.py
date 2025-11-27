import pytest
from unittest.mock import MagicMock, patch
from main import main
from config import Config

@patch("main.Config")
@patch("main.JobFinder")
@patch("main.JobHistory")
@patch("main.JobFilter")
@patch("main.FileManager")
def test_main_multiple_queries(mock_file_manager, mock_job_filter, mock_job_history, mock_job_finder, mock_config_class):
    """Test that main iterates over multiple queries and locations."""
    
    # Setup mock config
    mock_config = MagicMock()
    mock_config.api_key = "test_key"
    mock_config.queries = ["query1", "query2"]
    mock_config.locations = ["loc1", "loc2"]
    mock_config.search_params = {"q": "default", "location": "default"}
    mock_config.max_pages = 1
    mock_config.min_salary = 0
    mock_config.max_days_old = 30
    mock_config_class.return_value = mock_config
    
    # Setup mock finder
    mock_finder_instance = MagicMock()
    mock_finder_instance.search_jobs.return_value = []
    mock_finder_instance.removeDuplicates.return_value = []
    mock_job_finder.return_value = mock_finder_instance
    
    # Setup mock history
    mock_history_instance = MagicMock()
    mock_history_instance.is_seen.return_value = False
    mock_job_history.return_value = mock_history_instance

    # Setup mock filter
    mock_filter_instance = MagicMock()
    mock_filter_instance.is_valid.return_value = (True, "Valid")
    mock_job_filter.return_value = mock_filter_instance
    
    # Run main
    main()
    
    # Verify search_jobs calls
    # Expected calls: 2 queries * 2 locations = 4 calls
    assert mock_finder_instance.search_jobs.call_count == 4
    
    # Check call arguments
    calls = mock_finder_instance.search_jobs.call_args_list
    
    # Call 1: query1, loc1
    args1, _ = calls[0]
    # Assuming format_location_for_query returns "loc1" for "loc1"
    assert args1[0]["q"] == "query1 near loc1"
    assert args1[0]["location"] == "loc1"
    
    # Call 2: query1, loc2
    args2, _ = calls[1]
    assert args2[0]["q"] == "query1 near loc2"
    assert args2[0]["location"] == "loc2"
    
    # Call 3: query2, loc1
    args3, _ = calls[2]
    assert args3[0]["q"] == "query2 near loc1"
    assert args3[0]["location"] == "loc1"
    
    # Call 4: query2, loc2
    args4, _ = calls[3]
    assert args4[0]["q"] == "query2 near loc2"
    assert args4[0]["location"] == "loc2"
