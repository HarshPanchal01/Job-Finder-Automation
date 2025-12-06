import json
import logging
from unittest.mock import mock_open, patch, MagicMock
from file_manager import FileManager

def test_save_json():
    """Test saving data to JSON file."""
    logging.info("Testing save_json...")
    data = [{"id": 1}]
    filename = "test.json"
    
    with patch("builtins.open", mock_open()) as mock_file:
        FileManager.save_json(data, filename)
        
        mock_file.assert_called_once_with(filename, 'w')
        handle = mock_file()
        # Verify json.dump was called (by checking write calls)
        # Since json.dump writes chunks, we just check that write was called
        assert handle.write.called
    logging.info("save_json test passed.")

def test_save_markdown_grouping():
    """Test saving markdown with location grouping."""
    logging.info("Testing save_markdown with grouping...")
    jobs = [
        {
            "title": "Dev",
            "company_name": "A",
            "location": "Loc1",
            "search_location": "City X",
            "extensions": ["1 day ago"]
        },
        {
            "title": "Manager",
            "company_name": "B",
            "location": "Loc2",
            "search_location": "City Y",
            "extensions": ["2 days ago"]
        }
    ]
    filename = "test.md"
    
    with patch("builtins.open", mock_open()) as mock_file:
        FileManager.save_markdown(jobs, filename)
        
        mock_file.assert_called_once_with(filename, 'w', encoding="utf-8")
        handle = mock_file()
        
        # Check for key content in writes
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        assert "# Weekly Job Search Results" in written_content
        assert "## Summary" in written_content
        assert "| City X | 1 |" in written_content
        assert "### City X (1)" in written_content
        assert "<details>" in written_content
        assert "Dev" in written_content
        assert "Manager" in written_content
    logging.info("save_markdown grouping test passed.")

def test_save_markdown_empty():
    """Test saving markdown with no jobs."""
    logging.info("Testing save_markdown with empty list...")
    jobs = []
    filename = "test.md"
    
    with patch("builtins.open", mock_open()) as mock_file:
        FileManager.save_markdown(jobs, filename)
        
        handle = mock_file()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        assert "No jobs found this week." in written_content
    logging.info("save_markdown empty list test passed.")

def test_save_summary_markdown():
    """Test saving summary markdown (no details)."""
    logging.info("Testing save_summary_markdown...")
    jobs = [
        {
            "title": "Dev",
            "company_name": "A",
            "location": "Loc1",
            "search_location": "City X",
            "extensions": ["1 day ago"]
        }
    ]
    filename = "summary.md"
    
    with patch("builtins.open", mock_open()) as mock_file:
        FileManager.save_summary_markdown(jobs, filename)
        
        mock_file.assert_called_once_with(filename, 'w', encoding="utf-8")
        handle = mock_file()
        
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        
        assert "# Weekly Job Search Results (Summary)" in written_content
        assert "## Summary" in written_content
        assert "| City X | 1 |" in written_content
        # Ensure details are NOT present
        assert "### City X (1)" not in written_content
        assert "<details>" not in written_content
        assert "Dev" not in written_content # Title shouldn't be there
        assert "Please download the `jobs-report` artifact" in written_content
    logging.info("save_summary_markdown test passed.")
