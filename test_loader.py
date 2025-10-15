import unittest
import pandas as pd
from geo_loader import get_geolocator, fetch_location_data, build_geo_dataframe


class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        """
        Test that two known valid locations return approximately correct coordinates and types.
        """
        geolocator = get_geolocator(timeout=10)

        # Museum of Modern Art
        result1 = fetch_location_data(geolocator, "Museum of Modern Art")
        self.assertIsNotNone(result1, "Museum of Modern Art should return a valid result.")
        self.assertAlmostEqual(result1["latitude"], 40.7618552, delta=0.05)
        self.assertAlmostEqual(result1["longitude"], -73.9782438, delta=0.05)
        self.assertIn("museum", str(result1["type"]).lower(), "Type should include 'museum'.")

        # USS Alabama Battleship Memorial Park
        result2 = fetch_location_data(geolocator, "USS Alabama Battleship Memorial Park")
        self.assertIsNotNone(result2, "USS Alabama Battleship Memorial Park should return a valid result.")
        self.assertAlmostEqual(result2["latitude"], 30.684373, delta=0.05)
        self.assertAlmostEqual(result2["longitude"], -88.015316, delta=0.05)
        self.assertIn("park", str(result2["type"]).lower(), "Type should include 'park'.")

    def test_invalid_location(self):
        """
        Test that an invalid location returns NA values in the DataFrame
        except for the location name itself.
        """
        geolocator = get_geolocator(timeout=10)
        invalid_loc = "asdfqwer1234"

        # Build DataFrame with a single invalid location
        df = build_geo_dataframe(geolocator, [invalid_loc])

        # There should be exactly 1 row
        self.assertEqual(len(df), 1)

        # Location name is preserved
        self.assertEqual(df.loc[0, "location"], invalid_loc)

        # Latitude, longitude, and type are all NaN
        self.assertTrue(pd.isna(df.loc[0, "latitude"]), "Latitude should be NA for invalid location")
        self.assertTrue(pd.isna(df.loc[0, "longitude"]), "Longitude should be NA for invalid location")
        self.assertTrue(pd.isna(df.loc[0, "type"]), "Type should be NA for invalid location")


if __name__ == "__main__":
    unittest.main()
