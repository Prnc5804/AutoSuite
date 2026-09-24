"""
Login Page - Page Object for the TutorialsNinja Login Page.
Contains locators and methods for login functionality.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object representing the TutorialsNinja Login Page."""

    # ==================== LOCATORS ====================
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    FORGOTTEN_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten Password")
    LOGIN_PAGE_HEADING = (By.XPATH, "//h2[text()='Returning Customer']")

    # Error / Warning Messages
    ALERT_WARNING = (By.CSS_SELECTOR, "div.alert.alert-danger")

    # ==================== METHODS ====================

    def enter_email(self, email):
        """
        Enter email address in the login form.

        Args:
            email (str): Email address to enter.
        """
        self.logger.info(f"Entering email: {email}")
        self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """
        Enter password in the login form.

        Args:
            password (str): Password to enter.
        """
        self.logger.info("Entering password")
        self.type_text(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Click the 'Login' button to submit the login form."""
        self.logger.info("Clicking Login button")
        self.click_element(self.LOGIN_BUTTON)

    def login(self, email, password):
        """
        Perform a complete login with the given credentials.

        Args:
            email (str): Email address.
            password (str): Password.
        """
        self.logger.info(f"Logging in with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def get_warning_message(self):
        """
        Get the warning/error message displayed on login failure.

        Returns:
            str: Warning message text.
        """
        if self.is_element_displayed(self.ALERT_WARNING):
            msg = self.get_element_text(self.ALERT_WARNING)
            self.logger.info(f"Warning message: {msg}")
            return msg
        return ""

    def is_login_page_displayed(self):
        """Check if the login page heading is displayed."""
        return self.is_element_displayed(self.LOGIN_PAGE_HEADING)
