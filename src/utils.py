def format_location_for_query(location_str):
    """
    Formats a full location string (e.g., "Toronto, Ontario, Canada")
    into a shorter version for search queries (e.g., "Toronto, ON").
    
    Mappings for Canadian provinces and US states can be added here.
    """
    # Basic mapping for Canadian provinces and territories
    province_map = {
        "Ontario": "ON",
        "Quebec": "QC",
        "British Columbia": "BC",
        "Alberta": "AB",
        "Manitoba": "MB",
        "Saskatchewan": "SK",
        "Nova Scotia": "NS",
        "New Brunswick": "NB",
        "Newfoundland and Labrador": "NL",
        "Prince Edward Island": "PE",
        "Northwest Territories": "NT",
        "Yukon": "YT",
        "Nunavut": "NU"
    }
    
    # Basic mapping for US states
    state_map = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "District of Columbia": "DC",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY"
    }
    
    parts = [p.strip() for p in location_str.split(',')]
    
    if len(parts) >= 2:
        city = parts[0]
        region = parts[1]
        
        # Check if region is in our maps
        short_region = province_map.get(region) or state_map.get(region)
        
        if short_region:
            return f"{city}, {short_region}"
            
    # Fallback: return the first two parts if available, else original
    if len(parts) >= 2:
        return f"{parts[0]}, {parts[1]}"
        
    return location_str
