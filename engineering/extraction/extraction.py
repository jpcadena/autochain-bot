"""
A module for extraction in the engineering-extraction package.
"""
from pathlib import Path
from typing import Optional, Union

import pandas as pd

from core.file_manager import DataType
from core.persistence_manager import PersistenceManager


def extract_file(
    filename: Union[str, Path],
    data_type: Optional[DataType] = None,
) -> pd.DataFrame:
    """
    Engineering method to extract raw data from files
    :param filename: Filename to extract data from
    :type filename: Union[str, Path]
    :param data_type: The path where data will be saved.
    :type data_type: DataType
    :return: Dataframe with raw data
    :rtype: pd.DataFrame
    """
    dataframe: pd.DataFrame = PersistenceManager.load(
        filename=filename, data_type=data_type
    )
    return dataframe
