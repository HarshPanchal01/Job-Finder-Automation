import os
import json
import pytest
import logging
from datetime import datetime, timedelta
from unittest.mock import patch, mock_open
from job_history import JobHistory

@pytest.fixture
def temp_history_file(tmp_path):
    return tmp_path / "history.json"

def test_load_history_new_file(temp_history_file):
    """Test loading history when file does not exist."""
    logging.info("Testing load_history with new file...")
    history = JobHistory(history_file=str(temp_history_file))
    assert history.history == {}
    logging.info("load_history new file test passed.")

def test_load_history_existing_file(temp_history_file):
    """Test loading history from an existing file."""
    logging.info("Testing load_history with existing file...")
    data = {"job1": "2023-01-01T00:00:00"}
    with open(temp_history_file, 'w') as f:
        json.dump(data, f)
    
    history = JobHistory(history_file=str(temp_history_file))
    assert history.history == data
    logging.info("load_history existing file test passed.")

def test_save_history(temp_history_file):
    """Test saving history to file."""
    logging.info("Testing save_history...")
    history = JobHistory(history_file=str(temp_history_file))
    history.history = {"job1": "2023-01-01T00:00:00"}
    history.save_history()
    
    with open(temp_history_file, 'r') as f:
        data = json.load(f)
    assert data == {"job1": "2023-01-01T00:00:00"}
    logging.info("save_history test passed.")

def test_is_seen_and_add_job(temp_history_file):
    """Test checking if a job is seen and adding it."""
    logging.info("Testing is_seen and add_job...")
    history = JobHistory(history_file=str(temp_history_file))
    job = {"job_id": "123", "title": "Dev"}
    
    assert not history.is_seen(job)
    
    history.add_job(job)
    assert history.is_seen(job)
    assert "123" in history.history
    logging.info("is_seen and add_job test passed.")

def test_generate_id_fallback(temp_history_file):
    """Test ID generation when job_id is missing."""
    logging.info("Testing generate_id fallback...")
    history = JobHistory(history_file=str(temp_history_file))
    job = {"title": "Dev", "company_name": "Corp", "location": "NY"}
    
    # Should generate consistent hash
    id1 = history._generate_id(job)
    id2 = history._generate_id(job)
    assert id1 == id2
    assert len(id1) > 0
    logging.info("generate_id fallback test passed.")

def test_cleanup_old_entries(temp_history_file):
    """Test cleaning up old entries."""
    logging.info("Testing cleanup_old_entries...")
    history = JobHistory(history_file=str(temp_history_file))
    
    old_date = (datetime.now() - timedelta(days=100)).isoformat()
    new_date = datetime.now().isoformat()
    
    history.history = {
        "old_job": old_date,
        "new_job": new_date
    }
    
    history.cleanup_old_entries(days=90)
    
    assert "old_job" not in history.history
    assert "new_job" in history.history
    logging.info("cleanup_old_entries test passed.")
