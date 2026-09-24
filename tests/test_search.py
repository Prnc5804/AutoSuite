"""
Search Tests - Unittest Based
Tests for Product Search functionality on TutorialsNinja using unittest framework.
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
from pages.search_results_page import SearchResultsPage
from utilities.read_config import ReadConfig
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger
from utilities.screenshot_util import ScreenshotUtil


class TestProductSearch(unittest.TestCase):
    """Unittest test class for Product Search functionality."""

    logger = CustomLogger.get_logger()
    base_url = ReadConfig.get_base_url()

    @classmethod
    def setUpClass(cls):
        """Set up before all tests in this class."""
        cls.logger.info("=" * 60)
        cls.logger.info("STARTING PRODUCT SEARCH TESTS (Unittest)")
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
        self.search_results_page = SearchResultsPage(self.driver)

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
        cls.logger.info("COMPLETED PRODUCT SEARCH TESTS (Unittest)")
        cls.logger.info("=" * 60)

    # ==================== TEST CASES ====================

    def test_search_valid_product_macbook(self):
        """TC_SR_001: Verify search for a valid product 'MacBook'."""
        self.logger.info("TC_SR_001: Search for 'MacBook'")

        self.home_page.search_product("MacBook")

        self.assertTrue(
            self.search_results_page.is_search_results_page_displayed(),
            "Search results page is not displayed"
        )
        self.assertTrue(
            self.search_results_page.is_product_found("MacBook"),
            "MacBook not found in search results"
        )
        self.assertGreater(
            self.search_results_page.get_product_count(), 0,
            "No products found for 'MacBook'"
        )
        self.logger.info("TC_SR_001: PASSED - MacBook found in search results")

    def test_search_valid_product_imac(self):
        """TC_SR_002: Verify search for a valid product 'iMac'."""
        self.logger.info("TC_SR_002: Search for 'iMac'")

        self.home_page.search_product("iMac")

        self.assertTrue(
            self.search_results_page.is_product_found("iMac"),
            "iMac not found in search results"
        )
        self.logger.info("TC_SR_002: PASSED - iMac found in search results")

    def test_search_valid_product_iphone(self):
        """TC_SR_003: Verify search for a valid product 'iPhone'."""
        self.logger.info("TC_SR_003: Search for 'iPhone'")

        self.home_page.search_product("iPhone")

        self.assertTrue(
            self.search_results_page.is_product_found("iPhone"),
            "iPhone not found in search results"
        )
        self.logger.info("TC_SR_003: PASSED - iPhone found in search results")

    def test_search_invalid_product(self):
        """TC_SR_004: Verify search for a non-existent product."""
        self.logger.info("TC_SR_004: Search for non-existent product")

        self.home_page.search_product("xyznonexistent123")

        self.assertTrue(
            self.search_results_page.is_no_results_displayed(),
            "No results message not displayed for non-existent product"
        )
        self.assertEqual(
            self.search_results_page.get_product_count(), 0,
            "Products should not be found for non-existent search"
        )
        self.logger.info("TC_SR_004: PASSED - No results message shown for invalid search")

    def test_search_empty_query(self):
        """TC_SR_005: Verify search with an empty search term."""
        self.logger.info("TC_SR_005: Search with empty query")

        self.home_page.search_product("")

        self.assertTrue(
            self.search_results_page.is_search_results_page_displayed(),
            "Search results page not displayed for empty query"
        )
        self.assertTrue(
            self.search_results_page.is_no_results_displayed(),
            "No results message not displayed for empty search"
        )
        self.logger.info("TC_SR_005: PASSED - No results for empty search query")

    def test_search_results_page_title(self):
        """TC_SR_006: Verify the search results page title."""
        self.logger.info("TC_SR_006: Verify search results page title")

        self.home_page.search_product("MacBook")

        title = self.search_results_page.get_title()
        self.assertIn(
            "Search",
            title,
            f"Expected 'Search' in page title, got: {title}"
        )
        self.logger.info(f"TC_SR_006: PASSED - Search page title: {title}")

    def test_search_product_count(self):
        """TC_SR_007: Verify product count in search results for 'MacBook'."""
        self.logger.info("TC_SR_007: Verify product count for 'MacBook'")

        self.home_page.search_product("MacBook")

        count = self.search_results_page.get_product_count()
        self.assertGreater(
            count, 0,
            "Expected at least one product in search results"
        )
        self.logger.info(f"TC_SR_007: PASSED - Found {count} products for 'MacBook'")


class TestSearchDataDriven(unittest.TestCase):
    """Data-driven search tests using CSV test data."""

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
        self.search_results_page = SearchResultsPage(self.driver)

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

    def test_search_data_driven_from_csv(self):
        """Test product search using data from CSV file (data-driven)."""
        self.logger.info("Starting Data-Driven Search Tests from CSV")
        test_data = CSVReader.get_search_test_data()

        for data in test_data:
            test_id = data["test_id"]
            search_term = data["search_term"]
            expected = data["expected_result"]

            with self.subTest(test_id=test_id):
                self.logger.info(
                    f"{test_id}: Searching for '{search_term}' | expected={expected}"
                )

                # Navigate to home and search
                self.driver.get(self.base_url)
                self.home_page.search_product(search_term)

                if expected == "found":
                    self.assertTrue(
                        self.search_results_page.is_product_found(search_term),
                        f"{test_id}: Product '{search_term}' should be found"
                    )
                    self.logger.info(f"{test_id}: PASSED - '{search_term}' found as expected")
                else:
                    self.assertTrue(
                        self.search_results_page.is_no_results_displayed(),
                        f"{test_id}: No results message should be displayed for '{search_term}'"
                    )
                    self.logger.info(f"{test_id}: PASSED - No results for '{search_term}' as expected")


if __name__ == "__main__":
    unittest.main(verbosity=2)
