"""
Home Page - Page Object for the TutorialsNinja Home Page.
Contains locators and methods for the main landing page.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object representing the TutorialsNinja Home Page."""

    # ==================== LOCATORS ====================
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.btn.btn-default.btn-lg")
    MY_ACCOUNT_DROPDOWN = (By.XPATH, "//a[@title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    SHOPPING_CART_LINK = (By.XPATH, "//a[@title='Shopping Cart']")
    LOGO = (By.CSS_SELECTOR, "#logo a img")
    NAVBAR_LINKS = (By.CSS_SELECTOR, ".nav.navbar-nav > li > a")

    # ==================== METHODS ====================

    def click_my_account(self):
        """Click the 'My Account' dropdown link in the top navigation."""
        self.logger.info("Clicking 'My Account' dropdown")
        self.click_element(self.MY_ACCOUNT_DROPDOWN)

    def click_login_link(self):
        """Click the 'Login' link from the My Account dropdown."""
        self.logger.info("Navigating to Login page")
        self.click_my_account()
        self.click_element(self.LOGIN_LINK)

    def click_register_link(self):
        """Click the 'Register' link from the My Account dropdown."""
        self.logger.info("Navigating to Register page")
        self.click_my_account()
        self.click_element(self.REGISTER_LINK)

    def enter_search_text(self, search_term):
        """
        Enter a search term into the search bar.

        Args:
            search_term (str): Product name or keyword to search.
        """
        self.logger.info(f"Entering search term: {search_term}")
        self.type_text(self.SEARCH_INPUT, search_term)

    def click_search_button(self):
        """Click the search button to perform the search."""
        self.logger.info("Clicking search button")
        self.click_element(self.SEARCH_BUTTON)

    def search_product(self, product_name):
        """
        Perform a complete product search.

        Args:
            product_name (str): Product name or keyword to search.
        """
        self.logger.info(f"Searching for product: {product_name}")
        self.enter_search_text(product_name)
        self.click_search_button()

    def is_logo_displayed(self):
        """Check if the website logo is displayed."""
        return self.is_element_displayed(self.LOGO)

    def get_page_title(self):
        """Return the current page title."""
        return self.get_title()
