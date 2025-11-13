"""
Base Page Object Model
Provides common functionality for all page objects
"""
from playwright.sync_api import Page, expect
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects following POM pattern"""
    
    def __init__(self, page: Page):
        """
        Initialize base page
        
        Args:
            page: Playwright page instance
        """
        self.page = page
        self.timeout = 30000  # 30 seconds default timeout
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to specified URL
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="domcontentloaded")
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click element with optional custom timeout
        
        Args:
            selector: CSS selector or locator
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Clicking element: {selector}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.click(selector)
    
    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Fill input field with text
        
        Args:
            selector: CSS selector or locator
            text: Text to fill
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Filling element {selector} with: {text}")
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        self.page.fill(selector, text)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of element
        
        Args:
            selector: CSS selector or locator
            timeout: Custom timeout in milliseconds
            
        Returns:
            Text content of element
        """
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return self.page.text_content(selector)
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible
        
        Args:
            selector: CSS selector or locator
            timeout: Custom timeout in milliseconds
            
        Returns:
            True if visible, False otherwise
        """
        timeout = timeout or self.timeout
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_url(self, pattern: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match pattern
        
        Args:
            pattern: URL pattern to wait for
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for URL pattern: {pattern}")
        self.page.wait_for_url(pattern, timeout=timeout)
    
    def get_current_url(self) -> str:
        """
        Get current page URL
        
        Returns:
            Current URL
        """
        return self.page.url
    
    def wait_for_load_state(self, state: str = "load") -> None:
        """
        Wait for page load state
        
        Args:
            state: Load state to wait for (load, domcontentloaded, networkidle)
        """
        logger.info(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state)
    
    def screenshot(self, path: str) -> None:
        """
        Take screenshot of current page
        
        Args:
            path: Path to save screenshot
        """
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path)
    
    def press_key(self, selector: str, key: str) -> None:
        """
        Press keyboard key on element
        
        Args:
            selector: CSS selector or locator
            key: Key to press
        """
        logger.info(f"Pressing key {key} on element: {selector}")
        self.page.press(selector, key)
    
    def select_option(self, selector: str, value: str) -> None:
        """
        Select option from dropdown
        
        Args:
            selector: CSS selector or locator
            value: Value to select
        """
        logger.info(f"Selecting option {value} in: {selector}")
        self.page.select_option(selector, value)
    
    def check_checkbox(self, selector: str) -> None:
        """
        Check a checkbox
        
        Args:
            selector: CSS selector or locator
        """
        logger.info(f"Checking checkbox: {selector}")
        if not self.page.is_checked(selector):
            self.page.check(selector)
    
    def uncheck_checkbox(self, selector: str) -> None:
        """
        Uncheck a checkbox
        
        Args:
            selector: CSS selector or locator
        """
        logger.info(f"Unchecking checkbox: {selector}")
        if self.page.is_checked(selector):
            self.page.uncheck(selector)
    
    def hover(self, selector: str) -> None:
        """
        Hover over element
        
        Args:
            selector: CSS selector or locator
        """
        logger.info(f"Hovering over: {selector}")
        self.page.hover(selector)
    
    def wait_for_element(self, selector: str, state: str = "visible", timeout: Optional[int] = None) -> None:
        """
        Wait for element to reach specified state
        
        Args:
            selector: CSS selector or locator
            state: State to wait for (attached, detached, visible, hidden)
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Waiting for element {selector} to be {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout)