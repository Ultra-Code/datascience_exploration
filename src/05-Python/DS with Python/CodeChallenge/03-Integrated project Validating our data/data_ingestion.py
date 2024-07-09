"""
Add module for handing creating, quering and reading both CV files and sqlite db files
"""
import logging

import pandas as pd
from sqlalchemy import create_engine, text

# Name our logger so we know that logs from this module come from the data_ingestion module
logger = logging.getLogger("data_ingestion")
# Set a basic logging message up that prints out a timestamp, the name of our logger, and the message
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
db_path = "sqlite:///Maji_Ndogo_farm_survey_small.db"


def create_db_engine(db_path):
    """
    Create a database engine
    
    Parameters:
    db_path (str): A string containing the path to the database.

    Returns:
    object: A database engine used for performing queries.
    
    Example usage:
    field_df = query_data(create_db_engine(db_path), sql_query) 
    # Returns: field_df
    """
    try:
        engine = create_engine(db_path)
        # Test connection
        with engine.connect() as conn:
            pass
        # test if the database engine was created successfully
        logger.info("Database engine created successfully.")
        return engine  # Return the engine object if it all works well
    except (
        ImportError
    ):  # If we get an ImportError, inform the user SQLAlchemy is not installed
        logger.error(
            "SQLAlchemy is required to use this function. Please install it first."
        )
        raise e
    except Exception as e:  # If we fail to create an engine inform the user
        logger.error(f"Failed to create database engine. Error: {e}")
        raise e


def query_data(engine, sql_query):
    """
    Query a database engine to perform an sql query
    
    Parameters:
    engine (Object): a database engine created with A create_engine().
    sql_query (str): the query to be executed

    Returns:(void)
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
        logger.error(
            f"An error occurred while querying the database. Error: {e}"
        )
        raise e


def read_from_web_CSV(URL):
    """
    Reads a CSV from a remote link
    
    Parameters:
    URL (str): a link to a csv remotely hosted online.

    Returns:
        DataFrame: Add pandas dataframe representing the CSV file
    """
    try:
        df = pd.read_csv(URL)
        logger.info("CSV file read successfully from the web.")
        return df
    except pd.errors.EmptyDataError as e:
        logger.error(
            "The URL does not point to a valid CSV file. Please check the URL and try again."
        )
        raise e
    except Exception as e:
        logger.error(f"Failed to read CSV from the web. Error: {e}")
        raise e
