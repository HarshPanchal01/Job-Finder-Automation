import pytest
from unittest.mock import Mock
from job_filter import JobFilter

@pytest.fixture
def mock_config():
    config = Mock()
    config.blacklist_companies = ["bad company", "spam corp"]
    config.exclude_keywords = ["senior", "intern"]
    return config

def test_job_filter_valid_job(mock_config):
    """Test that a valid job passes the filter."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Good Company"
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_blacklisted_company(mock_config):
    """Test that a job from a blacklisted company is rejected."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Bad Company"
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Blacklisted company" in reason

def test_job_filter_blacklisted_company_case_insensitive(mock_config):
    """Test that company blacklist is case-insensitive."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "SPAM CORP"
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Blacklisted company" in reason

def test_job_filter_excluded_keyword(mock_config):
    """Test that a job with an excluded keyword in the title is rejected."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Senior Software Engineer",
        "company_name": "Good Company"
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Excluded keyword" in reason

def test_job_filter_excluded_keyword_case_insensitive(mock_config):
    """Test that keyword exclusion is case-insensitive."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer Intern",
        "company_name": "Good Company"
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Excluded keyword" in reason

def test_job_filter_partial_keyword_match(mock_config):
    """Test that partial keyword matches work (e.g. 'intern' in 'internship')."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineering Internship",
        "company_name": "Good Company"
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason is not None
    assert "Excluded keyword" in reason
