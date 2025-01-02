import logging
import os
import sys
from pathlib import Path
from typing import Final, cast

LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE: Final[bool | None] = os.getenv("LOG_FILE", "false") == "true"
LOG_DISABLE: Final[bool] = os.getenv("LOG_DISABLE", "false").lower() == "true"

LOG_FMT: Final[str] = "%(levelname)s : %(name)s : %(message)s : %(asctime)s"
LOG_SUCCESS_LEVEL: Final[int] = 25
LOG_RESET_COLOR: Final[str] = "\033[0m"
LOG_COLORS: Final[dict[str, str]] = {
    "DEBUG": "\033[94m",  # Blue
    "INFO": "\033[90m",  # Gray (changed)
    "SUCCESS": "\033[92m",  # Green (changed)
    "WARNING": "\033[93m",  # Yellow
    "ERROR": "\033[91m",  # Red
    "CRITICAL": "\033[95m",  # Magenta
}


class FALogger(logging.Logger):
    """FA Logger."""

    def __init__(self, name: str, level: int = logging.NOTSET) -> None:
        super().__init__(name, level)

    def success(self, message: str, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Log a success message."""
        if self.isEnabledFor(LOG_SUCCESS_LEVEL):
            self._log(LOG_SUCCESS_LEVEL, message, args, **kwargs)


class ColoredFormatter(logging.Formatter):
    """Logger formatter with colors."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with colors.

        Parameters
        ----------
        record: logging.LogRecord
            The log record to format.

        """
        color: str = LOG_COLORS.get(record.levelname, LOG_RESET_COLOR)
        formatted_message: str = super().format(record)

        return f"{color}{formatted_message}{LOG_RESET_COLOR}"


def __add_file_handler(path: Path) -> logging.FileHandler:
    """Add a file handler to the logger."""
    file_handler: logging.FileHandler = logging.FileHandler(path)
    file_format_output: logging.Formatter = logging.Formatter(LOG_FMT)
    file_handler.setFormatter(file_format_output)
    file_handler.setLevel(LOG_LEVEL)

    return file_handler


logging.addLevelName(LOG_SUCCESS_LEVEL, "SUCCESS")
logging.setLoggerClass(FALogger)

logger: FALogger = cast("FALogger", logging.getLogger("FALogger"))
logger.setLevel(logging.DEBUG)

if LOG_DISABLE:
    logging.disable(logging.CRITICAL)
else:
    stdout_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(ColoredFormatter(LOG_FMT))
    stdout_handler.setLevel(LOG_LEVEL)

    logger.addHandler(stdout_handler)

    if LOG_FILE:
        logger.addHandler(__add_file_handler(path=Path("../features-analyzer.log")))


logger.success("Logger initialized.")
