import pandas as pd
field_df = pd.read_csv('sampled_field_df.csv')


def test_read_field_dataframe_shape():
    # Test the shape of the DataFrame
    assert field_df.shape[1] == 18, "Field DataFrame shape is not as expected."

def test_field_dataframe_columns():
    # Test for the expected columns in the DataFrame
    expected_columns = [
        'Field_ID', 'Elevation', 'Latitude', 'Longitude', 'Location',
        'Slope', 'Rainfall', 'Min_temperature_C', 'Max_temperature_C',
        'Ave_temps', 'Soil_fertility', 'Soil_type', 'pH', 'Pollution_level',
        'Plot_size', 'Annual_yield', 'Crop_type', 'Standard_yield'
    ]
    assert all(column in field_df.columns for column in expected_columns), "Field DataFrame does not have the expected columns."

def test_field_dataframe_non_negative_elevation():
    # Test that all Elevation values are non-negative
    assert not (field_df['Elevation'] < 0).any(), "Elevation contains negative values."

def test_crop_types_are_valid():
    # Assuming 'Crop_type' is a column in your field DataFrame, and you have a predefined list of valid crop types
    valid_crop_types = ['cassava', 'tea', 'wheat', 'potato', 'banana', 'coffee', 'rice', 'maize']
    # Ensure all crop types are valid
    assert all(crop in valid_crop_types for crop in field_df['Crop_type']), "Invalid crop types found in DataFrame."