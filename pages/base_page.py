"""
Base Page - Parent class for all Page Objects.
Contains common methods used across all pages such as click, type, wait, etc.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException
)
from utilities.custom_logger import CustomLogger


class BasePage:
    """Base class for all Page Objects in the framework."""

    def __init__(self, driver):
        """
        Initialize BasePage with the WebDriver instance.

        Args:
            driver: Selenium WebDriver instance.
        """
        self.driver = driver
        self.logger = CustomLogger.get_logger()
        self.timeout = 10

    def open_url(self, url):
        """Navigate to a specific URL."""
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def get_title(self):
        """Return the current page title."""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title

    def get_current_url(self):
        """Return the current page URL."""
        url = self.driver.current_url
        self.logger.info(f"Current URL: {url}")
        return url

    def wait_for_element(self, locator, timeout=None):
        """
        Wait for an element to be visible on the page.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").
            timeout (int): Max wait time in seconds.

        Returns:
            WebElement: The located element.
        """
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found within {wait_time}s: {locator}")
            raise

    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for an element to be clickable.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").
            timeout (int): Max wait time in seconds.

        Returns:
            WebElement: The clickable element.
        """
        wait_time = timeout if timeout else self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable within {wait_time}s: {locator}")
            raise

    def click_element(self, locator):
        """
        Click on an element after waiting for it to be clickable.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").
        """
        self.logger.info(f"Clicking element: {locator}")
        element = self.wait_for_element_clickable(locator)
        element.click()

    def type_text(self, locator, text):
        """
        Clear a field and type text into it.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").
            text (str): Text to type into the element.
        """
        self.logger.info(f"Typing text into: {locator}")
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        """
        Get the text content of an element.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").

        Returns:
            str: Text content of the element.
        """
        element = self.wait_for_element(locator)
        text = element.text
        self.logger.info(f"Element text: {text}")
        return text

    def is_element_displayed(self, locator, timeout=5):
        """
        Check if an element is displayed on the page.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").
            timeout (int): Max wait time in seconds.

        Returns:
            bool: True if element is displayed, False otherwise.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            self.logger.info(f"Element not displayed: {locator}")
            return False

    def get_elements(self, locator, timeout=None):
        """
        Find multiple elements matching the locator.

        Args:
            locator (tuple): Locator tuple (By.xxx, "value").
            timeout (int): Max wait time in seconds.

        Returns:
            list[WebElement]: List of matching elements.
        """
        wait_time = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_all_elements_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            self.logger.info(f"Found {len(elements)} elements for: {locator}")
            return elements
        except TimeoutException:
            self.logger.info(f"No elements found for: {locator}")
            return []
