"""
A module for feature engineering in the engineering-transformation package.
"""
import pandas as pd


def engineer_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Apply feature engineering transformations to the dataframe.
    :param dataframe: Input dataframe
    :type dataframe: pd.DataFrame
    :return: Transformed dataframe with new features
    :rtype: pd.DataFrame
    """
    dataframe['new_feature'] = dataframe['existing_feature'] * 2
    return dataframe
