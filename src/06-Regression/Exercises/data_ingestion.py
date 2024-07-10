"""
This module provides utilities for database interactions and data loading from web resources.
It includes functions to create a database engine, execute SQL queries, and read CSV files from the web.
"""

import pandas as pd
from sqlalchemy import create_engine, text
import logging

# Set up basic logging configuration
logger = logging.getLogger('data_ingestion')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def create_db_engine(db_path):
    """
    Creates a database engine connection using SQLAlchemy.

    Parameters:
    - db_path (str): A database URL that indicates database dialect and connection arguments.

    Returns:
    - engine (Engine): An SQLAlchemy engine instance connected to the specified database.

    Raises:
    - ImportError: If the SQLAlchemy package is not installed.
    - Exception: For other issues that prevent database engine creation, including invalid db_path.

    Example:
    >>> engine = create_db_engine('sqlite:///my_database.db')
    """
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine # Return the engine object if it all works well
    except ImportError: #If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error("SQLAlchemy is required to use this function. Please install it first.")
        raise e
    except Exception as e:# If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e

def query_data(engine, sql_query):
    """
    Executes a SQL query and returns the results as a pandas DataFrame.

    Parameters:
    - engine (Engine): The SQLAlchemy engine to use for the query.
    - sql_query (str): The SQL query to execute.

    Returns:
    - DataFrame: A pandas DataFrame containing the results of the SQL query.

    Raises:
    - ValueError: If the SQL query fails (e.g., table not found).
    - Exception: For other issues, including problems with the connection.

    Example:
    >>> df = query_data(engine, "SELECT * FROM my_table")
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(sql_query), connection)
        if df.empty:
            # Log a message or handle the empty DataFrame scenario as needed
            msg = "The query returned an empty DataFrame."
            logger.error(msg)
            raise ValueError(msg)
        logger.info("Query executed successfully.")
        return df
    except ValueError as e: 
        logger.error(f"SQL query failed. Error: {e}")
        raise e
    except Exception as e:
        logger.error(f"An error occurred while querying the database. Error: {e}")
        raise e


def read_from_web_CSV(URL):
    """
    Reads a CSV file from a web URL into a pandas DataFrame.

    Parameters:
    - URL (str): The web URL to the CSV file.

    Returns:
    - DataFrame: A pandas DataFrame containing the data from the CSV file.

    Raises:
    - URLError: If the URL is unreachable or the host cannot be connected.
    - ValueError: If the URL does not point to a valid CSV file.
    - Exception: For other issues, including network problems.

    Example:
    >>> df = read_from_web_CSV("http://example.com/my_data.csv")
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error("The URL does not point to a valid CSV file. Please check the URL and try again.")
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e