import pytest
from date_parser import DateParser

@pytest.mark.parametrize("text,expected", [
    ("just now", 0),
    ("today", 0),
    ("1 hour ago", 0),
    ("yesterday", 1),
    ("2 days ago", 2),
    ("1 week ago", 7),
    ("2 weeks ago", 14),
    ("1 month ago", 30),
    ("2 months ago", 60),
    ("30+ days ago", 30),
    ("invalid date", None),
    ("", None),
    (None, None)
])
def test_parse_days_ago(text, expected):
    assert DateParser.parse_days_ago(text) == expected
