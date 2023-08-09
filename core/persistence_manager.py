"""
A module for persistence manager in the core package.
"""
import logging
from pathlib import Path
from typing import Optional, Union

import pandas as pd

from core.decorators import benchmark, with_logging
from core.file_manager import (
    CSVManager,
    DataType,
    DOCXManager,
    FileManager,
    XLSXManager,
)

logger: logging.Logger = logging.getLogger(__name__)


class PersistenceManager:
    """
    Persistence Manager to handle different file types.
    """

    managers: dict[str, FileManager] = {
        'xlsx': XLSXManager(),
        'csv': CSVManager(),
        'docx': DOCXManager(),
    }

    @classmethod
    @with_logging
    @benchmark
    def load(
        cls, filename: Union[str, Path], data_type: Optional[DataType] = None
    ) -> pd.DataFrame:
        """
        Load data from a file of given extension.
        :param filename: The name of the file including extension.
        :type filename: Union[str, Path]
        :param data_type: Path where data will be saved.
        :type data_type: Optional[DataType]
        :return: Dataframe retrieved from file.
        :rtype: pd.DataFrame
        """
        ext: str = str(filename).split('.')[-1]
        manager: Optional[FileManager] = cls.managers.get(ext)
        if manager:
            return manager.load(filename, data_type)
        else:
            raise ValueError(f"No manager found for extension {ext}")

    @classmethod
    @with_logging
    @benchmark
    def save(
        cls,
        dataframe: pd.DataFrame,
        data_type: Optional[DataType] = None,
        filename: str = "processed_data.xlsx",
    ) -> bool:
        """
        Save data to a file of given extension.
        :param dataframe: DataFrame to save.
        :type dataframe: pd.DataFrame
        :param data_type: Path where data will be saved.
        :type data_type: Optional[DataType]
        :param filename: Name of the file.
        :type filename: str
        :return: True if the file was created; otherwise false.
        :rtype: bool
        """
        ext: str = filename.split('.')[-1]
        manager: Optional[FileManager] = cls.managers.get(ext)
        return (
            manager.save(dataframe, data_type, filename) if manager else False
        )
