"""
Main script
"""
import logging

from core import logging_config
from core.decorators import benchmark

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


@benchmark
def main() -> None:
    """
    Main function to execute
    :return: None
    :rtype: NoneType
    """
    logger.info("Running main method")
    logger.info("Main successfully completed")


if __name__ == '__main__':
    logger.info("First log message")
    main()
    logger.info("End of the program execution")
