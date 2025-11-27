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
    assert config.search_params["q"] == "software developer"
    assert config.locations == ["Toronto, Ontario, Canada"]
    assert config.max_pages == 5
    assert config.min_salary == 0
    assert config.max_days_old == 7
    assert config.blacklist_companies == []
    assert config.exclude_keywords == []
    logging.info("Config defaults test passed.")

def test_config_env_vars(mock_env):
    """Test that Config loads values from environment variables."""
    logging.info("Testing Config environment variables...")
    with patch.dict(os.environ, {
        "API_KEY": "test_key",
        "GOOGLE_DOMAIN": "google.com",
        "SEARCH_QUERY": "python developer",
        "LOCATIONS": '["New York, New York, United States", "San Francisco, California, United States"]',
        "MAX_PAGES": "3",
        "MIN_SALARY": "80000",
        "MAX_DAYS_OLD": "14",
        "BLACKLIST_COMPANIES": '["Bad Corp", "Spam Inc"]',
        "EXCLUDE_KEYWORDS": '["Senior", "Lead"]'
    }):
        config = Config()
        assert config.api_key == "test_key"
        assert config.search_params["google_domain"] == "google.com"
        assert config.search_params["q"] == "python developer"
        assert config.locations == ["New York, New York, United States", "San Francisco, California, United States"]
        assert config.max_pages == 3
        assert config.min_salary == 80000
        assert config.max_days_old == 14
        assert config.blacklist_companies == ["Bad Corp", "Spam Inc"]
        assert config.exclude_keywords == ["Senior", "Lead"]
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
