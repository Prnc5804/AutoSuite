"""
Login Tests - PyTest Based
Tests for Login functionality on TutorialsNinja using pytest framework.
Uses Page Object Model, CSV test data, fixtures, markers, and screenshots on failure.
"""

import pytest
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utilities.read_config import ReadConfig
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger


@pytest.mark.login
@pytest.mark.usefixtures("setup")
class TestLoginPytest:
    """PyTest test class for Login functionality."""

    logger = CustomLogger.get_logger()

    # ==================== TEST CASES ====================

    @pytest.mark.smoke
    def test_login_valid_credentials(self):
        """TC_LG_001: Verify login with valid email and password."""
        self.logger.info("TC_LG_001: [PyTest] Test login with valid credentials")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)
        my_account_page = MyAccountPage(self.driver)

        home_page.click_login_link()
        assert login_page.is_login_page_displayed(), \
            "Login page is not displayed"

        email = ReadConfig.get_valid_email()
        password = ReadConfig.get_valid_password()
        login_page.login(email, password)

        assert my_account_page.is_my_account_page_displayed(), \
            "My Account page is not displayed after valid login"
        self.logger.info("TC_LG_001: PASSED")

    @pytest.mark.regression
    def test_login_invalid_credentials(self):
        """TC_LG_002: Verify login with invalid email and password."""
        self.logger.info("TC_LG_002: [PyTest] Test login with invalid credentials")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)

        home_page.click_login_link()
        login_page.login("invalid_user@test.com", "wrongpass")

        warning = login_page.get_warning_message()
        assert "Warning" in warning, \
            "Warning message not displayed for invalid credentials"
        self.logger.info("TC_LG_002: PASSED")

    @pytest.mark.regression
    def test_login_empty_email(self):
        """TC_LG_003: Verify login with empty email field."""
        self.logger.info("TC_LG_003: [PyTest] Test login with empty email")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)

        home_page.click_login_link()
        login_page.login("", "Test@12345")

        warning = login_page.get_warning_message()
        assert "Warning" in warning, \
            "Warning message not displayed for empty email"
        self.logger.info("TC_LG_003: PASSED")

    @pytest.mark.regression
    def test_login_empty_password(self):
        """TC_LG_004: Verify login with empty password field."""
        self.logger.info("TC_LG_004: [PyTest] Test login with empty password")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)

        home_page.click_login_link()
        login_page.login("seleniumtestuser2026@yopmail.com", "")

        warning = login_page.get_warning_message()
        assert "Warning" in warning, \
            "Warning message not displayed for empty password"
        self.logger.info("TC_LG_004: PASSED")

    @pytest.mark.regression
    def test_login_empty_fields(self):
        """TC_LG_005: Verify login with both fields empty."""
        self.logger.info("TC_LG_005: [PyTest] Test login with empty fields")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)

        home_page.click_login_link()
        login_page.login("", "")

        warning = login_page.get_warning_message()
        assert "Warning" in warning, \
            "Warning message not displayed for empty fields"
        self.logger.info("TC_LG_005: PASSED")

    @pytest.mark.smoke
    def test_login_page_title(self):
        """TC_LG_006: Verify the login page title."""
        self.logger.info("TC_LG_006: [PyTest] Test login page title")

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)

        home_page.click_login_link()

        title = login_page.get_title()
        assert "Account Login" in title, \
            f"Expected 'Account Login' in title, got: {title}"
        self.logger.info(f"TC_LG_006: PASSED - Title: {title}")


@pytest.mark.login
@pytest.mark.data_driven
@pytest.mark.usefixtures("setup")
class TestLoginDataDrivenPytest:
    """Data-driven login tests using CSV test data with PyTest."""

    logger = CustomLogger.get_logger()

    @pytest.mark.parametrize(
        "test_data",
        CSVReader.get_login_test_data(),
        ids=[row["test_id"] for row in CSVReader.get_login_test_data()]
    )
    def test_login_data_driven(self, test_data):
        """Data-driven login test using CSV data with pytest.mark.parametrize."""
        test_id = test_data["test_id"]
        email = test_data["email"]
        password = test_data["password"]
        expected = test_data["expected_result"]

        self.logger.info(
            f"{test_id}: [PyTest] Testing login | email={email} | expected={expected}"
        )

        home_page = HomePage(self.driver)
        login_page = LoginPage(self.driver)
        my_account_page = MyAccountPage(self.driver)

        home_page.click_login_link()
        login_page.login(email, password)

        if expected == "success":
            assert my_account_page.is_my_account_page_displayed(), \
                f"{test_id}: Login should succeed but My Account page not displayed"
            self.logger.info(f"{test_id}: PASSED - Login succeeded as expected")
        else:
            warning = login_page.get_warning_message()
            assert "Warning" in warning, \
                f"{test_id}: Login should fail but no warning displayed"
            self.logger.info(f"{test_id}: PASSED - Login failed as expected")
