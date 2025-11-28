import pytest
from unittest.mock import MagicMock
from job_filter import JobFilter

@pytest.fixture
def mock_config():
    config = MagicMock()
    config.blacklist_companies = ["Bad Corp"]
    config.exclude_keywords = ["Senior"]
    config.schedule_types = ["Full-time"]
    config.trusted_domains = ["linkedin", "glassdoor", "indeed"]
    return config

def test_job_filter_schedule_type_full_time(mock_config):
    """Test that Full-time jobs are valid."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Developer",
        "company_name": "Good Corp",
        "detected_extensions": {"schedule_type": "Full-time"},
        "apply_options": [{"title": "LinkedIn", "link": "https://linkedin.com/jobs/..."}]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_schedule_type_missing(mock_config):
    """Test that jobs with missing schedule_type are valid."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Developer",
        "company_name": "Good Corp",
        "detected_extensions": {},
        "apply_options": [{"title": "LinkedIn", "link": "https://linkedin.com/jobs/..."}]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_schedule_type_none(mock_config):
    """Test that jobs with None schedule_type are valid."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Developer",
        "company_name": "Good Corp",
        # No detected_extensions key at all
        "apply_options": [{"title": "LinkedIn", "link": "https://linkedin.com/jobs/..."}]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_schedule_type_contract(mock_config):
    """Test that Contract jobs are invalid when only Full-time is allowed."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Developer",
        "company_name": "Good Corp",
        "detected_extensions": {"schedule_type": "Contractor"}
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Invalid schedule type" in reason

def test_job_filter_schedule_type_part_time(mock_config):
    """Test that Part-time jobs are invalid when only Full-time is allowed."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Developer",
        "company_name": "Good Corp",
        "detected_extensions": {"schedule_type": "Part-time"}
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Invalid schedule type" in reason

def test_job_filter_schedule_type_custom_config(mock_config):
    """Test that custom schedule types are respected."""
    mock_config.schedule_types = ["Part-time", "Contract"]
    job_filter = JobFilter(mock_config)
    
    # Part-time should be valid now
    job_pt = {
        "title": "Developer",
        "company_name": "Good Corp",
        "detected_extensions": {"schedule_type": "Part-time"},
        "apply_options": [{"title": "LinkedIn", "link": "https://linkedin.com/jobs/..."}]
    }
    is_valid, reason = job_filter.is_valid(job_pt)
    assert is_valid is True
    
    # Full-time should be invalid now
    job_ft = {
        "title": "Developer",
        "company_name": "Good Corp",
        "detected_extensions": {"schedule_type": "Full-time"}
    }
    is_valid, reason = job_filter.is_valid(job_ft)
    assert is_valid is False
    assert "Invalid schedule type" in reason
