import logging
from job_parser import JobParser

def test_parse_job_full_data():
    """Test parsing a job with all fields present."""
    logging.info("Testing parse_job with full data...")
    raw_job = {
        "title": "Software Engineer",
        "company_name": "Tech Corp",
        "location": "Remote",
        "share_link": "http://example.com/job",
        "search_location": "Global",
        "extensions": ["2 days ago", "Full-time"]
    }
    
    parsed = JobParser.parse_job(raw_job)
    
    assert parsed["title"] == "Software Engineer"
    assert parsed["company"] == "Tech Corp"
    assert parsed["location"] == "Remote"
    assert parsed["link"] == "http://example.com/job"
    assert parsed["search_location"] == "Global"
    assert parsed["posted_date"] == "2 days ago"
    logging.info("parse_job full data test passed.")

def test_parse_job_missing_fields():
    """Test parsing a job with missing fields."""
    logging.info("Testing parse_job with missing fields...")
    raw_job = {}
    
    parsed = JobParser.parse_job(raw_job)
    
    assert parsed["title"] == "N/A"
    assert parsed["company"] == "N/A"
    assert parsed["location"] == "N/A"
    assert parsed["link"] is None
    assert parsed["search_location"] == "N/A"
    assert parsed["posted_date"] == "N/A"
    logging.info("parse_job missing fields test passed.")

def test_parse_job_posted_date_extraction():
    """Test extraction of posted date from extensions."""
    logging.info("Testing parse_job posted date extraction...")
    raw_job = {
        "extensions": ["Full-time", "3 days ago", "Apply on site"]
    }
    
    parsed = JobParser.parse_job(raw_job)
    assert parsed["posted_date"] == "3 days ago"
    logging.info("parse_job posted date extraction test passed.")

def test_parse_job_no_posted_date():
    """Test when no date-like string is in extensions."""
    logging.info("Testing parse_job with no posted date...")
    raw_job = {
        "extensions": ["Full-time", "Apply on site"]
    }
    
    parsed = JobParser.parse_job(raw_job)
    assert parsed["posted_date"] == "N/A"
    logging.info("parse_job no posted date test passed.")
