import re
import logging

class SalaryParser:
    @staticmethod
    def parse_salary(text):
        """
        Parses a salary string and returns a tuple (min_annual, max_annual).
        Returns None if no salary pattern is found.
        """
        if not text:
            return None

        text = text.lower().replace(',', '')
        
        # Check for frequency
        multiplier = 1
        if 'hour' in text or '/hr' in text:
            multiplier = 2080
        elif 'month' in text or '/mo' in text:
            multiplier = 12
        
        # Regex to find numbers (including k suffix)
        # Matches: $100k, 100000, 50.50
        # We look for numbers associated with currency symbols or just numbers if context implies
        # Simplified regex for "$X - $Y" or "$X"
        
        # Pattern: look for digits, optional decimals, optional 'k'
        # We want to capture the numeric part.
        # Examples: $50k, $50,000, 50000, 50.00
        
        matches = re.findall(r'\$?(\d+(?:\.\d+)?)(k)?', text)
        
        if not matches:
            return None

        values = []
        for amount, suffix in matches:
            try:
                val = float(amount)
                if suffix == 'k':
                    val *= 1000
                values.append(val)
            except ValueError:
                continue
        
        if not values:
            return None

        # Apply multiplier (hourly/monthly to annual)
        # Heuristic: If value is small (< 200) and no multiplier detected, it might be hourly but missing "hr"
        # But let's stick to explicit multiplier detection for safety, or the explicit logic requested.
        # "If hourly, rate * 2080"
        
        annual_values = [v * multiplier for v in values]
        
        min_sal = min(annual_values)
        max_sal = max(annual_values)
        
        return min_sal, max_sal

    @staticmethod
    def is_salary_text(text):
        """
        Checks if a string looks like a salary description.
        """
        text = text.lower()
        return any(x in text for x in ['$', 'salary', 'pay', 'compensation']) and \
               any(char.isdigit() for char in text)
