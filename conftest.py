"""
PyTest Configuration (conftest.py)
Contains fixtures for browser setup/teardown, screenshot on failure,
and pytest hooks for HTML reporting.
"""

import pytest
import os
import sys

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utilities.read_config import ReadConfig
from utilities.screenshot_util import ScreenshotUtil
from utilities.custom_logger import CustomLogger


logger = CustomLogger.get_logger()


# ==================== FIXTURES ====================

@pytest.fixture(scope="function")
def setup(request):
    """
    Fixture to set up and tear down the browser for each test.

    Yields:
        WebDriver: Selenium WebDriver instance.
    """
    browser = ReadConfig.get_browser().lower()
    logger.info(f"Setting up browser: {browser}")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.maximize_window()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(ReadConfig.get_implicit_wait())
    driver.get(ReadConfig.get_base_url())

    # Make driver accessible in the test
    if request.cls:
        request.cls.driver = driver
    if request.instance:
        request.instance.driver = driver

    yield driver

    # Teardown
    logger.info("Tearing down browser")
    driver.quit()


# ==================== PYTEST HOOKS ====================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    PyTest hook to capture screenshots on test failure.
    Also attaches screenshot to the HTML report if pytest-html is used.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Get the driver from the test instance
        driver = None
        if hasattr(item, "instance") and hasattr(item.instance, "driver"):
            driver = item.instance.driver
        elif hasattr(item, "cls") and hasattr(item.cls, "driver"):
            driver = item.cls.driver
        elif hasattr(item, "funcargs") and "setup" in item.funcargs:
            driver = item.funcargs["setup"]

        if driver:
            test_name = item.name
            logger.error(f"Test FAILED: {test_name} - Capturing screenshot")
            screenshot_path = ScreenshotUtil.take_screenshot(driver, test_name)

            # Attach screenshot to HTML report
            if screenshot_path and os.path.exists(screenshot_path):
                extra = getattr(report, "extras", [])
                try:
                    from pytest_html import extras as html_extras
                    extra.append(html_extras.image(screenshot_path))
                except ImportError:
                    # pytest-html extras not available - use basic extra
                    extra.append({"name": "Screenshot", "content": screenshot_path})
                report.extras = extra


def pytest_html_report_title(report):
    """Set the HTML report title."""
    report.title = "Selenium Automation Test Report - TutorialsNinja"


def pytest_configure(config):
    """Add custom markers to the pytest configuration."""
    config.addinivalue_line("markers", "login: Login test cases")
    config.addinivalue_line("markers", "search: Search test cases")
    config.addinivalue_line("markers", "smoke: Smoke test cases")
    config.addinivalue_line("markers", "regression: Regression test cases")
    config.addinivalue_line("markers", "data_driven: Data-driven test cases")
