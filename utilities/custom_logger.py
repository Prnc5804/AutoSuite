"""
Custom Logger Utility
Provides a configurable logger for test execution with file and console handlers.
"""

import logging
import os
from datetime import datetime


class CustomLogger:
    """Utility class to create and configure loggers for the framework."""

    @staticmethod
    def get_logger(name="automation_framework", log_level=logging.DEBUG):
        """
        Create and return a configured logger instance.

        Args:
            name (str): Name of the logger.
            log_level: Logging level (default: DEBUG).

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(name)

        # Avoid adding duplicate handlers
        if logger.handlers:
            return logger

        logger.setLevel(log_level)

        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "logs"
        )
        os.makedirs(logs_dir, exist_ok=True)

        # Log file with timestamp
        log_file = os.path.join(
            logs_dir,
            f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )

        # File Handler
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(log_level)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add Handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
