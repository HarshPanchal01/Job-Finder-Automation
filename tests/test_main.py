import pytest
from unittest.mock import MagicMock, patch
from main import main
from config import Config

@patch("main.Config")
@patch("main.JobFinder")
@patch("main.JobHistory")
@patch("main.JobFilter")
@patch("main.FileManager")
@patch("os.path.getsize")
@patch("shutil.copy")
def test_main_multiple_queries(mock_shutil_copy, mock_getsize, mock_file_manager, mock_job_filter, mock_job_history, mock_job_finder, mock_config_class):
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
    mock_config.email_address = None
    mock_config.email_password = None
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
    
    # Mock file size to be small so it tries to copy
    mock_getsize.return_value = 1000

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


@patch("main.EmailNotification")
@patch("datetime.datetime")
@patch("main.Config")
@patch("main.JobFinder")
@patch("main.JobHistory")
@patch("main.JobFilter")
@patch("main.FileManager")
@patch("os.path.getsize")
@patch("shutil.copy")
def test_main_email_subject_date_only(
    mock_shutil_copy,
    mock_getsize,
    mock_file_manager,
    mock_job_filter,
    mock_job_history,
    mock_job_finder,
    mock_config_class,
    mock_datetime,
    mock_email_notification,
):
    mock_config = MagicMock()
    mock_config.api_key = "test_key"
    mock_config.queries = []
    mock_config.locations = []
    mock_config.search_params = {"q": "default", "location": "default"}
    mock_config.max_pages = 1
    mock_config.min_salary = 0
    mock_config.max_days_old = 30
    mock_config.smtp_server = "smtp.test.com"
    mock_config.smtp_port = 587
    mock_config.email_address = "sender@test.com"
    mock_config.email_password = "password"
    mock_config.email_receivers = ["receiver@test.com"]
    mock_config_class.return_value = mock_config

    mock_finder_instance = MagicMock()
    mock_finder_instance.search_jobs.return_value = []
    mock_finder_instance.removeDuplicates.return_value = []
    mock_job_finder.return_value = mock_finder_instance

    mock_history_instance = MagicMock()
    mock_history_instance.is_seen.return_value = False
    mock_job_history.return_value = mock_history_instance

    mock_filter_instance = MagicMock()
    mock_filter_instance.is_valid.return_value = (True, "Valid")
    mock_job_filter.return_value = mock_filter_instance

    mock_getsize.return_value = 1000

    mock_datetime.now.return_value.strftime.return_value = "2026-01-01"

    main()

    email_instance = mock_email_notification.return_value
    email_instance.send_email.assert_called_once()

    args, _kwargs = email_instance.send_email.call_args
    assert args[1] == "Weekly Jobs Report - 2026-01-01"
    assert args[2] == "jobs.md"
