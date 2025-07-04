import logging
import os
from datetime import datetime
from settings import LOG_PATH, PROJECT_NAME

# Ensure the log directory exists only if LOCAL
os.makedirs(LOG_PATH, exist_ok=True)

# Create a log filename based on the current date
log_filename = datetime.now().strftime("%Y%m%d.log")
log_file_path = os.path.join(LOG_PATH, log_filename)


class ProjectNameFilter(logging.Filter):
    """
    A logging filter to add the project name to every log entry.
    """

    def filter(self, record):
        record.project = PROJECT_NAME
        return True


def configure_logging(enable_json_logs: bool = False):
    """
    Configures the root logger with handlers for both console and optionally file output.
    """
    # Create a logger
    logger = logging.getLogger(PROJECT_NAME)
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create formatter
    if enable_json_logs:
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "project": "%(project)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s %(project)s %(levelname)-4s %(message)s"
        )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler only if LOCAL
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Add custom filter
    logger.addFilter(ProjectNameFilter())

    return logger


logger = configure_logging()
