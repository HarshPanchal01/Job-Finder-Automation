import pytest
from utils import format_location_for_query

@pytest.mark.parametrize("input_loc, expected", [
    ("Toronto, Ontario, Canada", "Toronto, ON"),
    ("Vancouver, British Columbia, Canada", "Vancouver, BC"),
    ("New York, New York, United States", "New York, NY"),
    ("San Francisco, California, United States", "San Francisco, CA"),
    ("London, United Kingdom", "London, United Kingdom"), # Fallback
    ("Bangalore, Karnataka, India", "Bangalore, Karnataka, India"), # 3 parts, no truncation
    ("Paris, Île-de-France, France", "Paris, Île-de-France, France"), # 3 parts, no truncation
    ("CityOnly", "CityOnly"), # Fallback
    ("City, Region", "City, Region"), # Fallback
])
def test_format_location_for_query(input_loc, expected):
    assert format_location_for_query(input_loc) == expected
