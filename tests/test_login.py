"""
Login Tests - Unittest Based
Tests for Login functionality on TutorialsNinja using unittest framework.
Uses Page Object Model, CSV test data, and screenshots on failure.
"""

import unittest
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from utilities.read_config import ReadConfig
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger
from utilities.screenshot_util import ScreenshotUtil


class TestLogin(unittest.TestCase):
    """Unittest test class for Login functionality."""

    logger = CustomLogger.get_logger()
    base_url = ReadConfig.get_base_url()

    @classmethod
    def setUpClass(cls):
        """Set up the browser before all tests in this class."""
        cls.logger.info("=" * 60)
        cls.logger.info("STARTING LOGIN TESTS (Unittest)")
        cls.logger.info("=" * 60)

    def setUp(self):
        """Set up the browser before each test."""
        browser = ReadConfig.get_browser().lower()
        self.logger.info(f"Launching browser: {browser}")

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            self.driver.maximize_window()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        self.driver.implicitly_wait(ReadConfig.get_implicit_wait())
        self.driver.get(self.base_url)

        # Initialize Page Objects
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.my_account_page = MyAccountPage(self.driver)

    def _is_test_failed(self):
        """Check if THIS specific test instance failed or encountered an error."""
        result = getattr(self._outcome, 'result', None)
        if result and hasattr(result, 'failures') and hasattr(result, 'errors'):
            for test, _ in result.failures + result.errors:
                if test == self or getattr(test, 'test_case', None) == self:
                    return True
        return False

    def tearDown(self):
        """Clean up after each test - capture screenshot on failure."""
        if self._is_test_failed():
            test_name = self._testMethodName
            self.logger.error(f"Test FAILED: {test_name}")
            ScreenshotUtil.take_screenshot(self.driver, test_name)

        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests in this class."""
        cls.logger.info("=" * 60)
        cls.logger.info("COMPLETED LOGIN TESTS (Unittest)")
        cls.logger.info("=" * 60)

    # ==================== TEST CASES ====================

    def test_login_valid_credentials(self):
        """TC_LG_001: Verify login with valid email and password."""
        self.logger.info("TC_LG_001: Test login with valid credentials")

        self.home_page.click_login_link()
        self.assertTrue(
            self.login_page.is_login_page_displayed(),
            "Login page is not displayed"
        )

        email = ReadConfig.get_valid_email()
        password = ReadConfig.get_valid_password()
        self.login_page.login(email, password)

        self.assertTrue(
            self.my_account_page.is_my_account_page_displayed(),
            "My Account page is not displayed after valid login"
        )
        self.logger.info("TC_LG_001: PASSED - Login successful with valid credentials")

    def test_login_invalid_credentials(self):
        """TC_LG_002: Verify login with invalid email and password."""
        self.logger.info("TC_LG_002: Test login with invalid credentials")

        self.home_page.click_login_link()

        self.login_page.login("invalid_user@test.com", "wrongpass")

        warning = self.login_page.get_warning_message()
        self.assertIn(
            "Warning",
            warning,
            "Warning message not displayed for invalid credentials"
        )
        self.logger.info("TC_LG_002: PASSED - Warning displayed for invalid credentials")

    def test_login_empty_email(self):
        """TC_LG_003: Verify login with empty email field."""
        self.logger.info("TC_LG_003: Test login with empty email")

        self.home_page.click_login_link()

        self.login_page.login("", "Test@12345")

        warning = self.login_page.get_warning_message()
        self.assertIn(
            "Warning",
            warning,
            "Warning message not displayed for empty email"
        )
        self.logger.info("TC_LG_003: PASSED - Warning displayed for empty email")

    def test_login_empty_password(self):
        """TC_LG_004: Verify login with empty password field."""
        self.logger.info("TC_LG_004: Test login with empty password")

        self.home_page.click_login_link()

        self.login_page.login("seleniumtestuser2026@yopmail.com", "")

        warning = self.login_page.get_warning_message()
        self.assertIn(
            "Warning",
            warning,
            "Warning message not displayed for empty password"
        )
        self.logger.info("TC_LG_004: PASSED - Warning displayed for empty password")

    def test_login_empty_fields(self):
        """TC_LG_005: Verify login with both fields empty."""
        self.logger.info("TC_LG_005: Test login with empty email and password")

        self.home_page.click_login_link()

        self.login_page.login("", "")

        warning = self.login_page.get_warning_message()
        self.assertIn(
            "Warning",
            warning,
            "Warning message not displayed for empty fields"
        )
        self.logger.info("TC_LG_005: PASSED - Warning displayed for empty fields")

    def test_login_page_title(self):
        """TC_LG_006: Verify the login page title."""
        self.logger.info("TC_LG_006: Test login page title")

        self.home_page.click_login_link()

        title = self.login_page.get_title()
        self.assertIn(
            "Account Login",
            title,
            f"Expected 'Account Login' in title, got: {title}"
        )
        self.logger.info(f"TC_LG_006: PASSED - Login page title verified: {title}")


class TestLoginDataDriven(unittest.TestCase):
    """Data-driven login tests using CSV test data."""

    logger = CustomLogger.get_logger()
    base_url = ReadConfig.get_base_url()

    def setUp(self):
        """Set up the browser before each test."""
        browser = ReadConfig.get_browser().lower()

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
            self.driver.maximize_window()
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        self.driver.implicitly_wait(ReadConfig.get_implicit_wait())
        self.driver.get(self.base_url)

        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.my_account_page = MyAccountPage(self.driver)

    def _is_test_failed(self):
        """Check if THIS specific test instance failed or encountered an error."""
        result = getattr(self._outcome, 'result', None)
        if result and hasattr(result, 'failures') and hasattr(result, 'errors'):
            for test, _ in result.failures + result.errors:
                if test == self or getattr(test, 'test_case', None) == self:
                    return True
        return False

    def tearDown(self):
        """Clean up after each test."""
        if self._is_test_failed():
            test_name = self._testMethodName
            self.logger.error(f"Test FAILED: {test_name}")
            ScreenshotUtil.take_screenshot(self.driver, test_name)

        if self.driver:
            self.driver.quit()

    def test_login_data_driven_from_csv(self):
        """Test login using data from CSV file (data-driven)."""
        self.logger.info("Starting Data-Driven Login Tests from CSV")
        test_data = CSVReader.get_login_test_data()

        for data in test_data:
            test_id = data["test_id"]
            email = data["email"]
            password = data["password"]
            expected = data["expected_result"]

            with self.subTest(test_id=test_id):
                self.logger.info(
                    f"{test_id}: Testing login | email={email} | expected={expected}"
                )

                # Navigate to login page
                self.driver.get(self.base_url)
                self.home_page.click_login_link()

                # Perform login
                self.login_page.login(email, password)

                if expected == "success":
                    self.assertTrue(
                        self.my_account_page.is_my_account_page_displayed(),
                        f"{test_id}: Login should succeed but My Account page not displayed"
                    )
                    self.logger.info(f"{test_id}: PASSED - Login succeeded as expected")
                    # Logout for next iteration
                    self.my_account_page.logout()
                else:
                    warning = self.login_page.get_warning_message()
                    self.assertIn(
                        "Warning",
                        warning,
                        f"{test_id}: Login should fail but no warning displayed"
                    )
                    self.logger.info(f"{test_id}: PASSED - Login failed as expected")


if __name__ == "__main__":
    unittest.main(verbosity=2)
