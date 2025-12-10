import logging
import os
import sys
from typing import Optional

# Track whether we've configured a file handler on the root logger so we
# only add it once (when `log_file` is provided by the caller, typically
# from `main`). This lets all module-level loggers propagate to root and
# have their records written to the same file.
_root_file_configured = False


def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """Sets up a logger with the specified name and optional log file.

    Args:
        name: The name of the logger.
        log_file: Optional path to a log file. If provided, logs will be written to this file.

    Returns:
        logging.Logger: The configured logger instance.
    """
    global _root_file_configured

    logger = logging.getLogger(name)

    # Ensure logger level allows INFO messages
    logger.setLevel(logging.INFO)

    # If a log_file is provided, configure a single FileHandler on the
    # root logger so that all module loggers (which will propagate) write
    # to the same file. Do this once.
    if log_file and not _root_file_configured:
        root_logger = logging.getLogger()
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(logging.INFO)
        _root_file_configured = True

    # Only add console handler if this logger doesn't already have its own handlers.
    # We check `logger.handlers` (not hasHandlers) so that the presence of an
    # ancestor/root handler does not prevent adding our console handler.
    if logger.handlers:
        return logger

    # Console Handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Let records propagate to the root logger so the root FileHandler
    # (if configured) receives them and writes them to the log file.
    logger.propagate = True

    return logger
