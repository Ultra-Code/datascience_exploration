import pandas as pd
import pytest
from .field_data_processor import FieldDataProcessor
from .weather_data_processor import WeatherDataProcessor

config_params = {
    "sql_query": """
            SELECT *
            FROM geographic_features
            LEFT JOIN weather_features USING (Field_ID)
            LEFT JOIN soil_and_crop_features USING (Field_ID)
            LEFT JOIN farm_management_features USING (Field_ID)
        """,
    "db_path": "sqlite:///Maji_Ndogo_farm_survey_small.db",
    "columns_to_rename": {
        "Annual_yield": "Crop_type",
        "Crop_type": "Annual_yield",
    },
    "values_to_rename": {
        "cassaval": "cassava",
        "wheatn": "wheat",
        "teaa": "tea",
    },
    "weather_csv_path": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_station_data.csv",
    "weather_mapping_csv": "https://raw.githubusercontent.com/Explore-AI/Public-Data/master/Maji_Ndogo/Weather_data_field_mapping.csv",
    "regex_patterns": {
        "Rainfall": r"(\d+(\.\d+)?)\s?mm",
        "Temperature": r"(\d+(\.\d+)?)\s?C",
        "Pollution_level": r"=\s*(-?\d+(\.\d+)?)|Pollution at \s*(-?\d+(\.\d+)?)",
    },
}

field_processor = FieldDataProcessor(config_params)
field_processor.process()
field_df = field_processor.df

weather_processor = WeatherDataProcessor(config_params)
weather_processor.process()
weather_df = weather_processor.weather_df


@pytest.mark.skip(reason="Test is not yet implemented")
def test_read_weather_DataFrame_shape():
    assert weather_df.shape == (1843, 4), "Incorrect weather_df shape"


@pytest.mark.skip(reason="Test is not yet implemented")
def test_read_field_DataFrame_shape():
    assert field_df.shape == (5654, 19), "Incorrect field_df shape"


@pytest.mark.skip(reason="Test is not yet implemented")
def test_weather_DataFrame_columns():
    assert list(weather_df.columns) == [
        "Weather_station_ID",
        "Message",
        "Measurement",
        "Value",
    ], "The weather_df columns do not match"


@pytest.mark.skip(reason="Test is not yet implemented")
def test_field_DataFrame_columns():
    expected_columns = [
        "Field_ID",
        "Elevation",
        "Latitude",
        "Longitude",
        "Location",
        "Slope",
        "Rainfall",
        "Min_temperature_C",
        "Max_temperature_C",
        "Ave_temps",
        "Soil_fertility",
        "Soil_type",
        "pH",
        "Pollution_level",
        "Plot_size",
        "Annual_yield",
        "Crop_type",
        "Standard_yield",
        "Weather_station",
    ]
    assert (
        list(field_df.columns) == expected_columns
    ), "The field_df columns do not match"


@pytest.mark.skip(reason="Test is not yet implemented")
def test_field_DataFrame_non_negative_elevation():
    assert field_df[
        field_df["Elevation"] < 0
    ].empty, "There are negative numbers in Elevation column"


@pytest.mark.skip(reason="Test is not yet implemented")
def test_crop_types_are_valid():
    assert len(field_df["Crop_type"].unique()) == 8, "Incorrect length"


@pytest.mark.skip(reason="Test is not yet implemented")
def test_positive_rainfall_values():
    assert field_df[
        field_df["Rainfall"] < 0
    ].empty, "There are negativie Rainfall values"


import pandas as pd

field_df = pd.read_csv("sampled_field_df.csv")


def test_read_field_dataframe_shape():
    # Test the shape of the DataFrame
    assert field_df.shape[1] == 18, "Field DataFrame shape is not as expected."


def test_field_dataframe_columns():
    # Test for the expected columns in the DataFrame
    expected_columns = [
        "Field_ID",
        "Elevation",
        "Latitude",
        "Longitude",
        "Location",
        "Slope",
        "Rainfall",
        "Min_temperature_C",
        "Max_temperature_C",
        "Ave_temps",
        "Soil_fertility",
        "Soil_type",
        "pH",
        "Pollution_level",
        "Plot_size",
        "Annual_yield",
        "Crop_type",
        "Standard_yield",
    ]
    assert all(
        column in field_df.columns for column in expected_columns
    ), "Field DataFrame does not have the expected columns."


def test_field_dataframe_non_negative_elevation():
    # Test that all Elevation values are non-negative
    assert not (
        field_df["Elevation"] < 0
    ).any(), "Elevation contains negative values."


def test_crop_types_are_valid():
    # Assuming 'Crop_type' is a column in your field DataFrame, and you have a predefined list of valid crop types
    valid_crop_types = [
        "cassava",
        "tea",
        "wheat",
        "potato",
        "banana",
        "coffee",
        "rice",
        "maize",
    ]
    # Ensure all crop types are valid
    assert all(
        crop in valid_crop_types for crop in field_df["Crop_type"]
    ), "Invalid crop types found in DataFrame."
