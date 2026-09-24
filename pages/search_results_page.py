"""
Search Results Page - Page Object for the TutorialsNinja Search Results Page.
Contains locators and methods for verifying search results.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    """Page Object representing the TutorialsNinja Search Results Page."""

    # ==================== LOCATORS ====================
    SEARCH_PAGE_HEADING = (By.XPATH, "//h1[contains(text(),'Search')]")
    SEARCH_INPUT = (By.ID, "input-search")
    SEARCH_BUTTON = (By.ID, "button-search")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-layout")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-layout .caption h4 a")
    NO_RESULTS_MESSAGE = (
        By.XPATH,
        "//p[contains(text(),'There is no product that matches the search criteria')]"
    )
    PRODUCT_DESCRIPTIONS = (By.CSS_SELECTOR, ".product-layout .caption p:nth-child(2)")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-layout .price")
    ADD_TO_CART_BUTTONS = (
        By.CSS_SELECTOR,
        ".product-layout .button-group button:first-child"
    )

    # ==================== METHODS ====================

    def is_search_results_page_displayed(self):
        """
        Check if the search results page heading is displayed.

        Returns:
            bool: True if the search results page is visible.
        """
        return self.is_element_displayed(self.SEARCH_PAGE_HEADING)

    def get_search_heading_text(self):
        """
        Get the search results page heading text.

        Returns:
            str: Heading text (e.g., "Search - MacBook").
        """
        return self.get_element_text(self.SEARCH_PAGE_HEADING)

    def get_product_count(self):
        """
        Get the number of products displayed in search results.

        Returns:
            int: Number of product items found.
        """
        products = self.get_elements(self.PRODUCT_ITEMS, timeout=5)
        count = len(products)
        self.logger.info(f"Products found: {count}")
        return count

    def get_product_names(self):
        """
        Get a list of all product names displayed in the search results.

        Returns:
            list[str]: List of product name strings.
        """
        elements = self.get_elements(self.PRODUCT_NAMES, timeout=5)
        names = [elem.text for elem in elements]
        self.logger.info(f"Product names: {names}")
        return names

    def is_product_found(self, product_name):
        """
        Check if a specific product appears in the search results.

        Args:
            product_name (str): The product name to search for.

        Returns:
            bool: True if the product is found in results.
        """
        names = self.get_product_names()
        found = any(product_name.lower() in name.lower() for name in names)
        self.logger.info(f"Product '{product_name}' found: {found}")
        return found

    def is_no_results_displayed(self):
        """
        Check if the 'no product matches' message is displayed.

        Returns:
            bool: True if no results message is shown.
        """
        displayed = self.is_element_displayed(self.NO_RESULTS_MESSAGE)
        self.logger.info(f"No results message displayed: {displayed}")
        return displayed

    def search_again(self, search_term):
        """
        Perform another search from the search results page.

        Args:
            search_term (str): New search term.
        """
        self.logger.info(f"Searching again for: {search_term}")
        self.type_text(self.SEARCH_INPUT, search_term)
        self.click_element(self.SEARCH_BUTTON)
