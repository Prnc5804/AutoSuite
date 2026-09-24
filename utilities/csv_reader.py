"""
CSV Reader Utility
Reads test data from CSV files and returns it as a list of dictionaries.
"""

import csv
import os


class CSVReader:
    """Utility class to read test data from CSV files."""

    @staticmethod
    def read_csv(file_path):
        """
        Read a CSV file and return data as a list of dictionaries.

        Args:
            file_path (str): Absolute or relative path to the CSV file.

        Returns:
            list[dict]: Each row as a dictionary with column headers as keys.
        """
        data = []
        # Build absolute path relative to project root if not absolute
        if not os.path.isabs(file_path):
            project_root = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            file_path = os.path.join(project_root, file_path)

        with open(file_path, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(dict(row))
        return data

    @staticmethod
    def get_login_test_data():
        """Return login test data from the login_data.csv file, resolving environment credentials."""
        from utilities.read_config import ReadConfig
        data = CSVReader.read_csv(
            os.path.join("test_data", "login_data.csv")
        )
        valid_email = ReadConfig.get_valid_email()
        valid_password = ReadConfig.get_valid_password()

        for row in data:
            if row.get("email") in ("ENV_VALID_EMAIL", "${VALID_EMAIL}", "<VALID_EMAIL>"):
                row["email"] = valid_email
            if row.get("password") in ("ENV_VALID_PASSWORD", "${VALID_PASSWORD}", "<VALID_PASSWORD>"):
                row["password"] = valid_password
        return data

    @staticmethod
    def get_search_test_data():
        """Return search test data from the search_data.csv file."""
        return CSVReader.read_csv(
            os.path.join("test_data", "search_data.csv")
        )
