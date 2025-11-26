import pytest
from salary_parser import SalaryParser

@pytest.mark.parametrize("text,expected", [
    ("$100k - $120k", (100000, 120000)),
    ("$80,000 a year", (80000, 80000)),
    ("$50/hr", (104000, 104000)), # 50 * 2080
    ("$50 - $60 per hour", (104000, 124800)),
    ("$4000/month", (48000, 48000)),
    ("Competitive pay", None),
    ("", None),
    ("50k", (50000, 50000)),
    ("100k-150k", (100000, 150000)),
])
def test_parse_salary(text, expected):
    assert SalaryParser.parse_salary(text) == expected

def test_is_salary_text():
    assert SalaryParser.is_salary_text("$100k")
    assert SalaryParser.is_salary_text("Salary: 50000")
    assert not SalaryParser.is_salary_text("Full-time")
    assert not SalaryParser.is_salary_text("Remote")
