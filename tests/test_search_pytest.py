"""
Search Tests - PyTest Based
Tests for Product Search functionality on TutorialsNinja using pytest framework.
Uses Page Object Model, CSV test data, fixtures, markers, and screenshots on failure.
"""

import pytest
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utilities.read_config import ReadConfig
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger


@pytest.mark.search
@pytest.mark.usefixtures("setup")
class TestSearchPytest:
    """PyTest test class for Product Search functionality."""

    logger = CustomLogger.get_logger()

    # ==================== TEST CASES ====================

    @pytest.mark.smoke
    def test_search_valid_product_macbook(self):
        """TC_SR_001: Verify search for a valid product 'MacBook'."""
        self.logger.info("TC_SR_001: [PyTest] Search for 'MacBook'")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("MacBook")

        assert search_page.is_search_results_page_displayed(), \
            "Search results page is not displayed"
        assert search_page.is_product_found("MacBook"), \
            "MacBook not found in search results"
        assert search_page.get_product_count() > 0, \
            "No products found for 'MacBook'"
        self.logger.info("TC_SR_001: PASSED")

    @pytest.mark.smoke
    def test_search_valid_product_imac(self):
        """TC_SR_002: Verify search for a valid product 'iMac'."""
        self.logger.info("TC_SR_002: [PyTest] Search for 'iMac'")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("iMac")

        assert search_page.is_product_found("iMac"), \
            "iMac not found in search results"
        self.logger.info("TC_SR_002: PASSED")

    @pytest.mark.regression
    def test_search_valid_product_iphone(self):
        """TC_SR_003: Verify search for a valid product 'iPhone'."""
        self.logger.info("TC_SR_003: [PyTest] Search for 'iPhone'")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("iPhone")

        assert search_page.is_product_found("iPhone"), \
            "iPhone not found in search results"
        self.logger.info("TC_SR_003: PASSED")

    @pytest.mark.regression
    def test_search_invalid_product(self):
        """TC_SR_004: Verify search for a non-existent product."""
        self.logger.info("TC_SR_004: [PyTest] Search for non-existent product")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("xyznonexistent123")

        assert search_page.is_no_results_displayed(), \
            "No results message not displayed for non-existent product"
        assert search_page.get_product_count() == 0, \
            "Products should not be found for non-existent search"
        self.logger.info("TC_SR_004: PASSED")

    @pytest.mark.regression
    def test_search_empty_query(self):
        """TC_SR_005: Verify search with an empty search term."""
        self.logger.info("TC_SR_005: [PyTest] Search with empty query")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("")

        assert search_page.is_search_results_page_displayed(), \
            "Search results page not displayed for empty query"
        assert search_page.is_no_results_displayed(), \
            "No results message not displayed for empty search"
        self.logger.info("TC_SR_005: PASSED")

    @pytest.mark.smoke
    def test_search_results_page_title(self):
        """TC_SR_006: Verify the search results page title."""
        self.logger.info("TC_SR_006: [PyTest] Verify search results page title")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("MacBook")

        title = search_page.get_title()
        assert "Search" in title, \
            f"Expected 'Search' in page title, got: {title}"
        self.logger.info(f"TC_SR_006: PASSED - Title: {title}")

    @pytest.mark.regression
    def test_search_product_count(self):
        """TC_SR_007: Verify product count in search results for 'MacBook'."""
        self.logger.info("TC_SR_007: [PyTest] Verify product count for 'MacBook'")

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product("MacBook")

        count = search_page.get_product_count()
        assert count > 0, \
            "Expected at least one product in search results"
        self.logger.info(f"TC_SR_007: PASSED - Found {count} products")


@pytest.mark.search
@pytest.mark.data_driven
@pytest.mark.usefixtures("setup")
class TestSearchDataDrivenPytest:
    """Data-driven search tests using CSV test data with PyTest."""

    logger = CustomLogger.get_logger()

    @pytest.mark.parametrize(
        "test_data",
        CSVReader.get_search_test_data(),
        ids=[row["test_id"] for row in CSVReader.get_search_test_data()]
    )
    def test_search_data_driven(self, test_data):
        """Data-driven search test using CSV data with pytest.mark.parametrize."""
        test_id = test_data["test_id"]
        search_term = test_data["search_term"]
        expected = test_data["expected_result"]

        self.logger.info(
            f"{test_id}: [PyTest] Searching for '{search_term}' | expected={expected}"
        )

        home_page = HomePage(self.driver)
        search_page = SearchResultsPage(self.driver)

        home_page.search_product(search_term)

        if expected == "found":
            assert search_page.is_product_found(search_term), \
                f"{test_id}: Product '{search_term}' should be found"
            self.logger.info(f"{test_id}: PASSED - '{search_term}' found")
        else:
            assert search_page.is_no_results_displayed(), \
                f"{test_id}: No results message should be displayed for '{search_term}'"
            self.logger.info(f"{test_id}: PASSED - No results for '{search_term}'")
