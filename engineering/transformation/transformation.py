"""
A module for data transformation in the engineering-transformation package.
"""
import pandas as pd

from engineering.transformation.cleaning import clean_data
from engineering.transformation.feature_engineering import engineer_features


def transform_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Apply both cleaning and feature engineering transformations to the
     dataframe.
    :param dataframe: Input dataframe
    :type dataframe: pd.DataFrame
    :return: Transformed dataframe
    :rtype: pd.DataFrame
    """
    cleaned_data: pd.DataFrame = clean_data(dataframe)
    transformed_data: pd.DataFrame = engineer_features(cleaned_data)
    return transformed_data
