"""
A module for data engineering in the engineering package.
"""
from pathlib import Path
from typing import Optional, Union

import pandas as pd

from core.file_manager import DataType
from engineering.extraction.extraction import extract_file
from engineering.transformation.transformation import transform_data


def et_pipeline(
    filename: Union[str, Path], data_type: Optional[DataType] = DataType.RAW
) -> pd.DataFrame:
    """
    Execute the extraction and transformation (ET) pipeline.
    This pipeline first extracts raw data from the specified file and
     then applies data transformation steps, including cleaning and
      feature engineering.
    :param filename: Filename or path to extract data from
    :type filename: Union[str, Path]
    :param data_type: The path where data will be saved.
    :type data_type: DataType
    :return: Transformed dataframe after applying extraction and
     transformation steps
    :rtype: pd.DataFrame
    """
    raw_data: pd.DataFrame = extract_file(filename, data_type)
    transformed_data: pd.DataFrame = transform_data(raw_data)
    return transformed_data
