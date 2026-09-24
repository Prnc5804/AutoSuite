"""
My Account Page - Page Object for the TutorialsNinja My Account Page.
Displayed after successful login.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MyAccountPage(BasePage):
    """Page Object representing the TutorialsNinja My Account Page."""

    # ==================== LOCATORS ====================
    MY_ACCOUNT_HEADING = (By.XPATH, "//h2[text()='My Account']")
    EDIT_ACCOUNT_LINK = (By.LINK_TEXT, "Edit your account information.")
    CHANGE_PASSWORD_LINK = (By.LINK_TEXT, "Change your password")
    MY_ORDERS_LINK = (By.XPATH, "//a[contains(text(),'View your order history')]")
    LOGOUT_LINK_SIDEBAR = (By.XPATH, "//div[@class='list-group']//a[text()='Logout']")
    LOGOUT_LINK_DROPDOWN = (By.LINK_TEXT, "Logout")
    MY_ACCOUNT_DROPDOWN = (By.XPATH, "//a[@title='My Account']")

    # ==================== METHODS ====================

    def is_my_account_page_displayed(self):
        """
        Check if the 'My Account' page heading is displayed.

        Returns:
            bool: True if My Account page is displayed.
        """
        displayed = self.is_element_displayed(self.MY_ACCOUNT_HEADING)
        self.logger.info(f"My Account page displayed: {displayed}")
        return displayed

    def get_my_account_heading(self):
        """
        Get the text of the My Account heading.

        Returns:
            str: Heading text.
        """
        return self.get_element_text(self.MY_ACCOUNT_HEADING)

    def click_edit_account(self):
        """Click the 'Edit your account information' link."""
        self.logger.info("Clicking 'Edit Account'")
        self.click_element(self.EDIT_ACCOUNT_LINK)

    def click_change_password(self):
        """Click the 'Change your password' link."""
        self.logger.info("Clicking 'Change Password'")
        self.click_element(self.CHANGE_PASSWORD_LINK)

    def logout(self):
        """Logout from the application."""
        self.logger.info("Logging out")
        try:
            self.click_element(self.MY_ACCOUNT_DROPDOWN)
            self.click_element(self.LOGOUT_LINK_DROPDOWN)
        except Exception:
            try:
                self.click_element(self.LOGOUT_LINK_SIDEBAR)
            except Exception:
                base = self.driver.current_url.split("index.php")[0]
                self.driver.get(f"{base}index.php?route=account/logout")

    def logout_via_dropdown(self):
        """Logout from the application via the top dropdown."""
        self.logout()

