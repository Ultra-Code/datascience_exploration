"""
This module contains the FieldDataProcessor class, which is designed for processing agricultural field data. The class facilitates the ingestion of data from SQL databases, applies data cleaning and corrections, and performs analytical calculations like averaging measurements. It also integrates external weather station data to enrich the field data.

The class supports custom configuration for data processing, including column renaming, value corrections, and specifying target columns for aggregation calculations. It is equipped with logging capabilities to provide runtime information and debug insights.

Usage:
    Users can instantiate the FieldDataProcessor with a configuration dictionary specifying details for data processing and an optional logging level to control output verbosity.

    Example:
    ```python
    config_params = {
        'db_path': 'sqlite:///example.db',
        'sql_query': 'SELECT * FROM fields',
        'columns_to_rename': {'oldColumn': 'newColumn'},
        'values_to_rename': {'oldValue': 'newValue'},
        'weather_mapping_csv': 'path/to/weather_data.csv',
        'group_by_columns': ['Field_ID'],
        'target_columns': ['Temperature', 'Rainfall']
    }
    processor = FieldDataProcessor(config_params, logging_level="DEBUG")
    processed_df = processor.process()
    ```
"""

import pandas as pd
from data_ingestion import create_db_engine, query_data, read_from_web_CSV
import logging

class FieldDataProcessor:
    """
    A class to process agricultural field data with capabilities for data ingestion, cleaning, corrections, and analytical calculations.

    Attributes:
        db_path (str): Database path for SQL data ingestion.
        sql_query (str): SQL query for data selection.
        columns_to_rename (dict): Specifies column renaming mappings.
        values_to_rename (dict): Specifies mappings for correcting measurement values.
        weather_map_data (str): URL or path to the weather station CSV data.
        group_by_columns (list): Columns to group by when calculating means.
        target_columns (list): Target columns for mean calculation.
        engine (SQLAlchemy Engine): Database engine for SQL operations.
        df (pandas DataFrame): The processed data.
        logger (logging.Logger): Logger for the class.

    Methods:
        set_logging_level(logging_level): Sets the logging level for the class instance.
        ingest_sql_data(): Ingests data from an SQL database.
        rename_columns(df): Renames columns in the provided DataFrame.
        correct_crop_type(crop): Corrects crop types based on predefined mappings.
        apply_corrections(df): Applies corrections to the DataFrame.
        calculate_means(): Calculates mean values for specified columns.
        weather_station_mapping(): Loads weather station data.
        process(): Executes the data processing pipeline.
    """
    def __init__(self, config_params, logging_level="INFO"): # When we instantiate this class, we can optionally specify what logs we want to see

        # Initialising class with attributes we need. Refer to the code above to understand how each attribute relates to the code
        self.db_path = config_params['db_path']
        self.sql_query = config_params['sql_query']
        self.columns_to_rename = config_params['columns_to_rename']
        self.values_to_rename = config_params['values_to_rename']
        self.weather_map_data = config_params['weather_mapping_csv']
        # Configuration for calculating means could be added here if necessary
        self.engine = None  # Database engine
        self.df = None
        self.initialize_logging(logging_level)
        
    # This method enables logging in the class.
    def initialize_logging(self, logging_level):
        """
        Sets up logging for this instance of FieldDataProcessor.
        """
        logger_name = __name__ + ".FieldDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False  # Prevents log messages from being propagated to the root logger

        # Set logging level
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":  # Option to disable logging
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO  # Default to INFO

        self.logger.setLevel(log_level)

        # Only add handler if not already added to avoid duplicate messages
        if not self.logger.handlers:
            ch = logging.StreamHandler()  # Create console handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        # Use self.logger.info(), self.logger.debug(), etc.

    def ingest_sql_data(self):
        """
        Ingests data from a SQL database based on the configured database path and SQL query.

        Utilizes the SQLAlchemy engine to connect to the database and execute the provided SQL query. The result
        is loaded into a pandas DataFrame, making it ready for further processing.

        Returns:
        - A pandas DataFrame containing the data fetched from the database.
        """
        self.engine = create_db_engine(self.db_path)
        self.df = query_data(self.engine, self.sql_query)
        self.logger.info("Sucessfully loaded data.")
    
    def rename_columns(self):
        """
        Swaps the names of two columns in the DataFrame based on the configuration specified in columns_to_rename.
        
        This method specifically addresses the use case where two column names need to be exchanged.
        """
        # Temporarily rename one of the columns to avoid a naming conflict
        temp_name = "__temp_name_for_swap__"
        while temp_name in self.df.columns:
            temp_name += "_"
        
        # Extract the columns to rename from the configuration
        column1, column2 = list(self.columns_to_rename.keys())[0], list(self.columns_to_rename.values())[0]
        
        # Perform the swap
        self.df = self.df.rename(columns={column1: temp_name, column2: column1})
        self.df = self.df.rename(columns={temp_name: column2})
        
        self.logger.info(f"Swapped columns: {column1} with {column2}")

    def apply_corrections(self, column_name='Crop_type', abs_column='Elevation'):
        """
        Applies corrections to the DataFrame based on mappings specified in values_to_rename.

        This method focuses on correcting values in a specified column, often used for standardizing or
        correcting categorical data such as crop types.

        Parameters:
        - df (pandas DataFrame): The DataFrame to apply corrections to.
        - column_name (str): The name of the column to correct.

        Returns:
        - The DataFrame with corrections applied to the specified column.
        """
            # Ensures Elevation values are non-negative

        self.df[abs_column] = self.df[abs_column].abs()

        self.df[column_name] = self.df[column_name].apply(lambda crop: self.values_to_rename.get(crop, crop))
        self.df[column_name] = self.df[column_name].apply(lambda x: x.strip())
    
    def weather_station_mapping(self):
        """
        Loads external weather station data from a CSV file, specified by weather_map_data.

        This method enriches the field data with external weather information by merging the weather data
        based on common identifiers. It is an essential step in correlating field observations with weather
        conditions.

        Returns:
        - The weather station data as a pandas DataFrame.
        """
        weather_map_df = read_from_web_CSV(self.weather_map_data)
        self.df = self.df.merge(weather_map_df, on='Field_ID', how='left')
        self.df = self.df.drop(columns="Unnamed: 0")
        
    def process(self):
        """
        Applies corrections to the DataFrame based on mappings specified in values_to_rename.

        This method focuses on correcting values in a specified column, often used for standardizing or
        correcting categorical data such as crop types.

        Parameters:
        - df (pandas DataFrame): The DataFrame to apply corrections to.
        - column_name (str): The name of the column to correct.

        Returns:
        - The DataFrame with corrections applied to the specified column.
        """
        self.ingest_sql_data()
        self.rename_columns()
        self.apply_corrections()
        self.weather_station_mapping()

