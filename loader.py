
import time
from geopy.geocoders import Nominatim
import pandas as pd


def get_geolocator(agent='h501-student', timeout=10):
    """
    Initiate a Nominatim geolocator instance with a given agent and timeout.
    """
    return Nominatim(user_agent=agent, timeout=timeout)


def fetch_location_data(geolocator, loc):
    """
    Fetch latitude, longitude, and type for a given location.
    If the location does not exist, return NaN for numeric/text fields except the location name.
    """
    try:
        location = geolocator.geocode(loc)

        if location is None:
            # Invalid location → return NaN for latitude, longitude, type
            return {
                "location": loc,
                "latitude": float('nan'),
                "longitude": float('nan'),
                "type": float('nan')
            }

        # Safe access to type
        loc_type = location.raw.get('type', float('nan'))

        return {
            "location": loc,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "type": loc_type
        }

    except Exception:
        # Any unexpected error → treat as invalid location
        return {
            "location": loc,
            "latitude": float('nan'),
            "longitude": float('nan'),
            "type": float('nan')
        }


def build_geo_dataframe(geolocator, locations, pause_between=1.0):
    """
    Build a pandas DataFrame of geocoded locations.
    pause_between: seconds to wait between requests to avoid hitting rate limits.
    """
    results = []
    for loc in locations:
        data = fetch_location_data(geolocator, loc)
        results.append(data)
        time.sleep(pause_between)  # polite pause to respect Nominatim usage policy

    df = pd.DataFrame(results, columns=["location", "latitude", "longitude", "type"])
    return df


if __name__ == "__main__":
    geolocator = get_geolocator()

    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",       # invalid / garbage string
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa"
    ]

    df = build_geo_dataframe(geolocator, locations)

    print(df)
    df.to_csv("./geo_data.csv", index=False)
    print("Saved ./geo_data.csv")
