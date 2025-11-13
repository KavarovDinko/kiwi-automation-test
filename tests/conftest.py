"""
Pytest configuration and fixtures
Handles browser setup, teardown, and shared fixtures
"""
import pytest
from playwright.sync_api import Page, BrowserContext, Browser, Playwright
from typing import Generator
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """
    Browser launch arguments
    Can be customized for different environments
    """
    return {
        "headless": False,  # Set to True for CI/CD
        "slow_mo": 500,  # Slow down operations for visibility
    }


@pytest.fixture(scope="session")
def browser_context_args():
    """
    Browser context arguments
    Configure viewport, locale, etc.
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone_id": "Europe/Amsterdam",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Create a new page for each test
    
    Yields:
        Page instance
    """
    page = context.new_page()
    
    # Set default timeout
    page.set_default_timeout(30000)
    
    yield page
    
    # Cleanup
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only for failed tests in call phase
    if report.when == "call" and report.failed:
        try:
            # Get the page fixture from the test
            page = item.funcargs.get('page')
            if page:
                # Create screenshots directory if it doesn't exist
                screenshot_dir = "reports/screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                
                # Generate screenshot filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"{screenshot_dir}/{item.name}_{timestamp}.png"
                
                # Take screenshot
                page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
                
                # Attach to HTML report
                extra = getattr(report, 'extra', [])
                extra.append(pytest.html.extras.image(screenshot_path))
                report.extra = extra
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


def pytest_configure(config):
    """
    Configure pytest
    """
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    
    # Add custom markers
    config.addinivalue_line(
        "markers", "smoke: Mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: Mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "one_way: Mark test as one-way flight test"
    )