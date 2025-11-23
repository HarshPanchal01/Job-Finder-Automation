from src.config import Config
import json

def debug_config():
    print("--- Debugging Configuration ---")
    
    # Initialize configuration
    try:
        config = Config()
        print("Configuration loaded successfully.")
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    # Check API Key (masked)
    if config.api_key:
        masked_key = config.api_key[:4] + "*" * (len(config.api_key) - 8) + config.api_key[-4:]
        print(f"API_KEY: {masked_key}")
    else:
        print("API_KEY: Not found!")

    # Print Search Parameters
    print("\n--- Search Parameters (Base) ---")
    print(json.dumps(config.search_params, indent=2))

    # Print Locations
    print("\n--- Locations to Search ---")
    if hasattr(config, 'locations'):
        print(f"Total Locations: {len(config.locations)}")
        for i, loc in enumerate(config.locations, 1):
            print(f"{i}. {loc}")
            
            # Simulate what the API call params would look like
            simulated_params = config.search_params.copy()
            simulated_params["location"] = loc
            print(f"   -> API Call Params: q='{simulated_params.get('q')}', location='{simulated_params.get('location')}'")
    else:
        print("No locations found in config.")

    print("\n--- End Debug ---")

if __name__ == "__main__":
    debug_config()
