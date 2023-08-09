"""
A module for config in the core package.
"""
from functools import lru_cache

from pydantic import BaseSettings, PositiveInt


class Settings(BaseSettings):
    """
    Settings class based on Pydantic Base Settings
    """

    PROJECT_NAME: str = "autochain-bot"
    MAX_COLUMNS: PositiveInt = 50
    WIDTH: PositiveInt = 1000
    ENCODING: str = "UTF-8"
    CHUNK_SIZE: PositiveInt = 5000
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    DATETIME_FORMAT: str = "%d.%m.%Y"
    FILE_DATETIME_FORMAT: str = "%d-%b-%Y-%H-%M-%S"
    LOG_FORMAT: str = (
        "[%(name)s][%(asctime)s][%(levelname)s][%(module)s]"
        "[%(funcName)s][%(lineno)d]: %(message)s"
    )
    NUMERICS: list[str] = [
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "int8",
        "int16",
        "int32",
        "int64",
        "float16",
        "float32",
        "float64",
    ]
    PALETTE: str = "pastel"
    FONT_SIZE: PositiveInt = 15
    FIG_SIZE: tuple[PositiveInt, PositiveInt] = (15, 8)
    RE_PATTERN: str = "([a-z])([A-Z])"
    RE_REPL: str = r"\g<1> \g<2>"

    class Config:
        """
        Config class for Settings
        """

        env_file: str = ".env"
        env_file_encoding: str = 'utf-8'
        arbitrary_types_allowed: bool = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get settings cached
    :return: The settings instance
    :rtype: Settings
    """
    return Settings()


settings: Settings = Settings()
