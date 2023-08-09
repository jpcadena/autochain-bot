"""
A module for data cleaning in the engineering-transformation package.
"""
import pandas as pd


def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Apply cleaning transformations to the dataframe.
    :param dataframe: Input dataframe
    :type dataframe: pd.DataFrame
    :return: Cleaned dataframe
    :rtype: pd.DataFrame
    """
    dataframe.dropna(inplace=True)
    return dataframe
