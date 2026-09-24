"""
Screenshot Utility
Captures and saves screenshots on test failure for debugging purposes.
"""

import os
from datetime import datetime


class ScreenshotUtil:
    """Utility class to capture screenshots during test execution."""

    @staticmethod
    def take_screenshot(driver, test_name="test"):
        """
        Capture a screenshot and save it to the screenshots directory.

        Args:
            driver: Selenium WebDriver instance.
            test_name (str): Name of the test for the screenshot filename.

        Returns:
            str: Absolute path to the saved screenshot file.
        """
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        # Capture and save screenshot
        try:
            driver.save_screenshot(filepath)
            print(f"[Screenshot] Saved: {filepath}")
        except Exception as e:
            print(f"[Screenshot] Failed to capture screenshot: {e}")

        return filepath
