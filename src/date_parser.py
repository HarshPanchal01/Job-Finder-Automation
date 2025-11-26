import re

class DateParser:
    @staticmethod
    def parse_days_ago(text):
        """
        Parses a relative date string and returns the number of days ago.
        Returns None if the date cannot be parsed.
        """
        if not text:
            return None
            
        text = text.lower().strip()
        
        # Immediate matches
        if any(x in text for x in ['just now', 'today', 'hour', 'minute', 'second']):
            return 0
        if 'yesterday' in text:
            return 1
            
        # Regex for "X days/weeks/months ago"
        # Matches: "2 days ago", "1 week ago", "30+ days ago"
        match = re.search(r'(\d+)\+?\s*(day|week|month)', text)
        if match:
            number = int(match.group(1))
            unit = match.group(2)
            
            if 'day' in unit:
                return number
            elif 'week' in unit:
                return number * 7
            elif 'month' in unit:
                return number * 30
                
        return None
