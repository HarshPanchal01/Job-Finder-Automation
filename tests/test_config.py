import os
import json
import pytest
import logging
from unittest.mock import patch
from config import Config

@pytest.fixture
def mock_env():
    # Patch os.environ to be empty
    with patch.dict(os.environ, {}, clear=True):
        # Also patch load_dotenv to do nothing, so it doesn't read from .env file
        with patch("config.load_dotenv"):
            yield

def test_config_defaults(mock_env):
    """Test that Config uses default values when env vars are missing."""
    logging.info("Testing Config defaults...")
    config = Config()
    assert config.api_key is None
    assert config.search_params["google_domain"] == "google.ca"
    # q is no longer set by default in search_params, it's built dynamically
    assert "q" not in config.search_params or config.search_params["q"] is None
    assert config.locations == ["Toronto, Ontario, Canada"]
    assert config.max_pages == 5
    assert config.min_salary == 0
    assert config.max_days_old == 7
    assert config.blacklist_companies == []
    assert config.exclude_keywords == []
    assert config.schedule_types == ["full-time"]
    assert config.queries == ["software developer"]
    assert config.smtp_server == "smtp.gmail.com"
    assert config.smtp_port == 587
    assert config.email_address is None
    assert config.email_receivers == []
    logging.info("Config defaults test passed.")

def test_config_env_vars(mock_env):
    """Test that Config loads values from environment variables."""
    logging.info("Testing Config environment variables...")
    with patch.dict(os.environ, {
        "API_KEY": "test_key",
        "GOOGLE_DOMAIN": "google.com",
        "SEARCH_QUERIES": '["data scientist", "machine learning engineer"]',
        "LOCATIONS": '["New York, New York, United States", "San Francisco, California, United States"]',
        "MAX_PAGES": "3",
        "MIN_SALARY": "80000",
        "MAX_DAYS_OLD": "14",
        "BLACKLIST_COMPANIES": '["Bad Corp", "Spam Inc"]',
        "EXCLUDE_KEYWORDS": '["Senior", "Lead"]',
        "SCHEDULE_TYPES": '["Part-time", "Contract"]',
        "SMTP_SERVER": "smtp.test.com",
        "SMTP_PORT": "465",
        "EMAIL_ADDRESS": "sender@test.com",
        "EMAIL_PASSWORD": "password123",
        "EMAIL_RECEIVER": '["rec1@test.com", "rec2@test.com"]'
    }):
        config = Config()
        assert config.api_key == "test_key"
        assert config.search_params["google_domain"] == "google.com"
        assert config.queries == ["data scientist", "machine learning engineer"]
        assert config.locations == ["New York, New York, United States", "San Francisco, California, United States"]
        assert config.max_pages == 3
        assert config.min_salary == 80000
        assert config.max_days_old == 14
        assert config.blacklist_companies == ["Bad Corp", "Spam Inc"]
        assert config.exclude_keywords == ["Senior", "Lead"]
        assert config.schedule_types == ["Part-time", "Contract"]
        assert config.smtp_server == "smtp.test.com"
        assert config.smtp_port == 465
        assert config.email_address == "sender@test.com"
        assert config.email_password == "password123"
        assert config.email_receivers == ["rec1@test.com", "rec2@test.com"]
    logging.info("Config environment variables test passed.")

def test_config_locations_single_string(mock_env):
    """Test fallback for LOCATIONS as a single string."""
    logging.info("Testing Config locations single string fallback...")
    with patch.dict(os.environ, {"LOCATIONS": "London, United Kingdom"}):
        config = Config()
        assert config.locations == ["London, United Kingdom"]
    logging.info("Config locations single string fallback test passed.")

def test_config_locations_invalid_json(mock_env):
    """Test fallback for LOCATIONS with invalid JSON."""
    logging.info("Testing Config locations invalid JSON fallback...")
    with patch.dict(os.environ, {"LOCATIONS": "['Invalid JSON'"}):
        config = Config()
        assert config.locations == ["['Invalid JSON'"]
    logging.info("Config locations invalid JSON fallback test passed.")

def test_config_max_pages_invalid(mock_env):
    """Test fallback for MAX_PAGES with invalid integer."""
    logging.info("Testing Config max_pages invalid integer fallback...")
    with patch.dict(os.environ, {"MAX_PAGES": "invalid"}):
        config = Config()
        assert config.max_pages == 5
    logging.info("Config max_pages invalid integer fallback test passed.")

def test_config_blacklist_comma_separated(mock_env):
    """Test fallback for BLACKLIST_COMPANIES as comma-separated string."""
    logging.info("Testing Config blacklist comma-separated fallback...")
    with patch.dict(os.environ, {"BLACKLIST_COMPANIES": "Bad Corp, Spam Inc"}):
        config = Config()
        assert config.blacklist_companies == ["Bad Corp", "Spam Inc"]
    logging.info("Config blacklist comma-separated fallback test passed.")
