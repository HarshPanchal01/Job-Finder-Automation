import pytest
from unittest.mock import Mock
from job_filter import JobFilter

@pytest.fixture
def mock_config():
    config = Mock()
    config.blacklist_companies = []
    config.exclude_keywords = []
    config.schedule_types = ["full-time"]
    config.trusted_domains = ["linkedin", "glassdoor", "indeed", "ziprecruiter", "simplyhired"]
    return config

def test_job_filter_source_linkedin(mock_config):
    """Test that a job with a LinkedIn source is accepted."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": [
            {"title": "LinkedIn", "link": "https://www.linkedin.com/jobs/view/..."}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_source_glassdoor(mock_config):
    """Test that a job with a Glassdoor source is accepted."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": [
            {"title": "Glassdoor", "link": "https://www.glassdoor.com/job/..."}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_source_indeed(mock_config):
    """Test that a job with an Indeed source is accepted."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": [
            {"title": "Indeed", "link": "https://ca.indeed.com/viewjob?..."}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_source_company_direct(mock_config):
    """Test that a job with a direct company link is accepted."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Acme Corp",
        "apply_options": [
            {"title": "Apply on Acme Corp", "link": "https://careers.acmecorp.com/job/123"}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_source_generic_aggregator(mock_config):
    """Test that a job with only generic aggregators is rejected."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": [
            {"title": "Techjobs.ca", "link": "https://www.techjobs.ca/job/..."},
            {"title": "BeBee CA", "link": "https://ca.bebee.com/job/..."}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason == "No reputable application source found"

def test_job_filter_source_no_options(mock_config):
    """Test that a job with no apply options is rejected."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": []
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason == "No application options found"

def test_job_filter_source_company_name_match_complex(mock_config):
    """Test company name matching with spaces/normalization."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "The Best Company",
        "apply_options": [
            {"title": "Apply", "link": "https://thebestcompany.com/careers"}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_source_company_name_in_path_should_reject(mock_config):
    """Company name appearing only in the URL path should NOT count as a direct company site."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Advanced Trading Systems Developer",
        "company_name": "beBeeSoftware",
        "apply_options": [
            {
                "title": "Jobilize",
                "link": "https://www.jobilize.com/job/ca-on-toronto-advanced-trading-systems-developer-bebeesoftware-hiring",
            }
        ],
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is False
    assert reason == "No reputable application source found"

def test_job_filter_source_ziprecruiter(mock_config):
    """Test that a job with a ZipRecruiter source is accepted."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": [
            {"title": "ZipRecruiter", "link": "https://www.ziprecruiter.com/job/..."}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None

def test_job_filter_source_simplyhired(mock_config):
    """Test that a job with a SimplyHired source is accepted."""
    job_filter = JobFilter(mock_config)
    job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "apply_options": [
            {"title": "SimplyHired", "link": "https://www.simplyhired.com/job/..."}
        ]
    }
    is_valid, reason = job_filter.is_valid(job)
    assert is_valid is True
    assert reason is None
