"""
Configuration Reader Utility
Reads configuration values from config/config.ini using configparser.
"""

import configparser
import os
from dotenv import load_dotenv

# Load environment variables from .env file at project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))


class ReadConfig:
    """Utility class to read configuration values from .env and config.ini."""

    _config = None
    _config_path = os.path.join(project_root, "config", "config.ini")

    @classmethod
    def _load_config(cls):
        """Load the configuration file if not already loaded."""
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            cls._config.read(cls._config_path)

    @classmethod
    def get_base_url(cls):
        """Return the base URL of the application under test."""
        return os.getenv("BASE_URL") or (cls._load_config() or cls._config.get("common", "base_url"))

    @classmethod
    def get_browser(cls):
        """Return the browser name from configuration."""
        return os.getenv("BROWSER") or (cls._load_config() or cls._config.get("common", "browser"))

    @classmethod
    def get_implicit_wait(cls):
        """Return the implicit wait time in seconds."""
        cls._load_config()
        return int(cls._config.get("common", "implicit_wait"))

    @classmethod
    def get_valid_email(cls):
        """Return the valid test email from .env or configuration."""
        env_val = os.getenv("VALID_EMAIL")
        if env_val:
            return env_val
        cls._load_config()
        return cls._config.get("credentials", "valid_email", fallback="")

    @classmethod
    def get_valid_password(cls):
        """Return the valid test password from .env or configuration."""
        env_val = os.getenv("VALID_PASSWORD")
        if env_val:
            return env_val
        cls._load_config()
        return cls._config.get("credentials", "valid_password", fallback="")

    @classmethod
    def get_screenshots_dir(cls):
        """Return the screenshots directory path."""
        cls._load_config()
        return cls._config.get("paths", "screenshots_dir")

    @classmethod
    def get_reports_dir(cls):
        """Return the reports directory path."""
        cls._load_config()
        return cls._config.get("paths", "reports_dir")

    @classmethod
    def get_logs_dir(cls):
        """Return the logs directory path."""
        cls._load_config()
        return cls._config.get("paths", "logs_dir")

    @classmethod
    def get_test_data_dir(cls):
        """Return the test data directory path."""
        cls._load_config()
        return cls._config.get("paths", "test_data_dir")
