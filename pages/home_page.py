"""
Kiwi.com Homepage Page Object Model
Contains all locators and methods for homepage interactions
"""
from pages.base_page import BasePage
from playwright.sync_api import Page
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Page Object Model for Kiwi.com homepage"""
    
    # URL
    URL = "https://www.kiwi.com/en/"
    
    def __init__(self, page: Page):
        """
        Initialize homepage
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        logger.info("Homepage POM initialized")
    
    def open(self) -> None:
        """Navigate to Kiwi.com homepage"""
        self.navigate_to(self.URL)
        self.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)
        self._handle_cookie_consent()
    
    def _handle_cookie_consent(self) -> None:
        """Handle cookie consent popup if present"""
        try:
            # Try multiple cookie button selectors
            cookie_selectors = [
                "button:has-text('Accept')",
                "button:has-text('Accept all')",
                "button:has-text('OK')",
                "[data-test='CookiesPopup-Accept']",
                "#cookies-accept"
            ]
            
            for selector in cookie_selectors:
                try:
                    if self.is_visible(selector, timeout=3000):
                        logger.info(f"Clicking cookie consent: {selector}")
                        self.click(selector)
                        self.page.wait_for_timeout(1000)
                        return
                except Exception:
                    continue
                    
            logger.info("No cookie consent popup found or already accepted")
        except Exception as e:
            logger.info(f"Cookie consent handling: {e}")
    
    def select_trip_type(self, trip_type: str) -> None:
        """
        Select trip type (one-way)
        
        Args:
            trip_type: Type of trip ('one-way')
        """
        logger.info(f"Selecting trip type: {trip_type}")
        
        try:
            # Wait for page to be ready
            self.page.wait_for_timeout(1000)
            
            if trip_type.lower() in ['one-way', 'oneway', 'one way']:
                # Multiple approaches to find one-way button
                trip_type_selectors = [
                    "button:has-text('One-way')",
                    "button:has-text('one-way')",
                    "//button[contains(translate(., 'ONEWAY', 'oneway'), 'one-way')]",
                    "[data-test='TripTypeButton-one-way']",
                    "label:has-text('One-way')",
                    "input[value='one-way']",
                    "[data-test='SearchFormModesPicker-active-return']"
                ]

                trip_types = "[data-test='ModePopupOption-oneWay']"
                
                for selector in trip_type_selectors:
                    try:
                        logger.info(f"Trying trip_type selector: {selector}")
                        if self.is_visible(selector, timeout=2000):
                            self.click(selector)
                            logger.info(f"✓ trip_type selected with: {selector}")
                            self.page.wait_for_timeout(500)
                            self.click(trip_types)
                            logger.info(f"✓ One-way selected")
                            return
                    except Exception as e:
                        logger.debug(f"Selector {selector} failed: {e}")
                        continue
                
                logger.warning("Could not find one-way button, may already be selected")    
        except Exception as e:
            logger.error(f"Error selecting trip type: {e}")
    
    def set_departure_airport(self, airport_code: str) -> None:
        """
        Set departure airport with improved reliability
        
        Args:
            airport_code: Airport code (e.g., 'RTM')
        """
        logger.info(f"Setting departure airport: {airport_code}")
        
        try:
            # Wait a bit for page to be ready
            self.page.wait_for_timeout(1000)
            
            # Try different selectors for departure field
            departure_selectors = [
                "[data-test='SearchField-input']:first-of-type"
            ]
            
            clear_departure_preselected_items = "[data-test='PlacePickerInput-origin'] [data-test='PlacePickerInputPlace-close']"

            for selector in departure_selectors:
                try:
                    logger.info(f"Trying departure selector: {selector}")
                    
                    if self.is_visible(selector, timeout=2000):
                        # Clear and fill
                        self.click(selector)
                        self.page.wait_for_timeout(500)
                        
                        # Clear existing value
                        try:
                            if self.is_visible(clear_departure_preselected_items, timeout=1000):
                                self.click(clear_departure_preselected_items)
                                self.page.wait_for_timeout(500)
                        except Exception:
                            pass
                        
                        self.page.fill(selector, "")
                        self.page.wait_for_timeout(300)
                        
                        # Type slowly
                        self.page.type(selector, airport_code, delay=100)
                        self.page.wait_for_timeout(1500)
                        
                        logger.info(f"✓ Typed {airport_code} in departure field")
                        
                        # Press Enter to confirm
                        self.page.keyboard.press("Enter")
                        self.page.wait_for_timeout(1000)
                        
                        # Extra wait to ensure dropdown closes
                        logger.info("Waiting for arrival dropdown to close...")
                        self.page.wait_for_timeout(1500)
                        return
                        
                except Exception as e:
                    logger.debug(f"Departure selector {selector} failed: {e}")
                    continue
            
            logger.error("Could not find departure airport input field")
            
        except Exception as e:
            logger.error(f"Error setting departure airport: {e}")
    
    def set_arrival_airport(self, airport_code: str) -> None:
        """
        Set arrival airport with improved reliability
        
        Args:
            airport_code: Airport code (e.g., 'MAD')
        """
        logger.info(f"Setting arrival airport: {airport_code}")
        
        try:
            self.page.wait_for_timeout(1000)
            
            # Try different selectors for arrival field
            arrival_selectors = [
                "[data-test='PlacePickerInput-destination'] [data-test='SearchField-input']",
                "[data-test='SearchField-input'][data-test*='destination']",
                "[data-test='PlacePickerInputPlace']:last-child input",
                "input[placeholder*='To']",
                "input[placeholder*='Where to']"
            ]
            
            for selector in arrival_selectors:
                try:
                    logger.info(f"Trying arrival selector: {selector}")
                    
                    if self.is_visible(selector, timeout=2000):
                        # Clear and fill
                        self.click(selector)
                        self.page.wait_for_timeout(500)
                        
                        # Clear existing value
                        self.page.fill(selector, "")
                        self.page.wait_for_timeout(300)
                        
                        # Type slowly
                        self.page.type(selector, airport_code, delay=100)
                        self.page.wait_for_timeout(1500)
                        
                        logger.info(f"✓ Typed {airport_code} in arrival field")
                        
                        # Press Enter to confirm
                        self.page.keyboard.press("Enter")
                        self.page.wait_for_timeout(500)
                        return
                        
                except Exception as e:
                    logger.debug(f"Arrival selector {selector} failed: {e}")
                    continue
            
            logger.error("Could not find arrival airport input field")
            
        except Exception as e:
            logger.error(f"Error setting arrival airport: {e}")
    
    def set_departure_date(self, weeks_from_now: int = 1) -> None:
        """
        Set departure date - WORKING VERSION based on debug findings
        
        Args:
            weeks_from_now: Number of weeks from current date
        """
        logger.info(f"Setting departure date: {weeks_from_now} week(s) from now")
        
        try:
            target_date = datetime.now() + timedelta(weeks=weeks_from_now)
            target_day_str = str(target_date.day)
            
            logger.info(f"Target date: {target_date.strftime('%Y-%m-%d')} (day: {target_day_str})")
            
            # Step 1: Close any open dropdowns
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1000)
            
            # Step 2: Click date field to open calendar
            date_field_selector = "[data-test='SearchDateInput']"
            logger.info(f"Clicking date field: {date_field_selector}")
            
            element = self.page.locator(date_field_selector).first
            element.scroll_into_view_if_needed()
            element.click()
            logger.info("✓ Calendar opened")
            
            # Step 3: Wait for calendar to load
            self.page.wait_for_timeout(3000)
            
            # Step 4: Select the date
            self._select_date_from_calendar(target_day_str)
            
            # Step 5: Click "Set dates" button
            self._click_set_dates_button()
            
            logger.info(f"✓ Departure date set successfully")
            
        except Exception as e:
            logger.error(f"Failed to set departure date: {e}")
            self.page.screenshot(path=f"reports/screenshots/date_error.png")
            raise
    
    def _select_date_from_calendar(self, target_day_str: str) -> None:
        """
        Select exact single day - uses the WORKING selector from debug
        
        Args:
            target_day_str: Day as string (e.g., '25')
        """
        logger.info(f"Selecting day: {target_day_str}")
        
        try:
            # Wait for calendar to fully load
            self.page.wait_for_timeout(3000)
            
            # Find div with specific classes and exact text match
            logger.info(f"Looking for clickable div with text '{target_day_str}'")
            
            # Get all elements containing the day number
            all_day_elements = self.page.locator(f"div:has-text('{target_day_str}')").all()
            logger.info(f"Found {len(all_day_elements)} divs containing '{target_day_str}'")
            
            clicked = False
            for i, elem in enumerate(all_day_elements):
                try:
                    # Get element details
                    text = elem.inner_text().strip()
                    classes = elem.get_attribute("class") or ""
                    
                    # Match EXACT text (not '125' or '250') and look for date cell classes
                    if text == target_day_str:
                        logger.info(f"Candidate {i}: text='{text}', classes='{classes[:80]}...'")
                        
                        # Check if it's a date cell
                        if ("font-bold" in classes and "text-large" in classes) or \
                        ("leading-normal" in classes and "text-ink" in classes):
                            
                            # Check it's not disabled
                            if "disabled" not in classes.lower() and elem.is_visible():
                                logger.info(f"  → Clicking candidate {i}...")
                                elem.click()
                                logger.info(f"✓ Successfully clicked day {target_day_str}!")
                                clicked = True
                                self.page.wait_for_timeout(1500)
                                return
                except Exception as e:
                    logger.debug(f"Candidate {i} failed: {e}")
                    continue
            
            if not clicked:
                logger.error(f"Could not click day {target_day_str}")
                # Take screenshot for debugging
                self.page.screenshot(path=f"reports/screenshots/day_{target_day_str}_not_found.png")
                raise Exception(f"Date {target_day_str} not found or not clickable")
                
        except Exception as e:
            logger.error(f"Error selecting date: {e}")
            raise
    
    def _click_set_dates_button(self) -> None:
        """Click 'Set dates' button to confirm"""
        logger.info("Clicking 'Set dates' button")
        
        try:
            self.page.wait_for_timeout(1000)
            
            set_dates_selector = "[data-test='SearchFormDoneButton']"
            
            element = self.page.locator(set_dates_selector).first
            if element.is_visible(timeout=3000):
                element.click()
                logger.info("✓ Clicked 'Set dates' button")
                self.page.wait_for_timeout(2000)
            else:
                logger.warning("Set dates button not visible, pressing Enter")
                self.page.keyboard.press("Enter")
                self.page.wait_for_timeout(1500)
                
        except Exception as e:
            logger.warning(f"Error clicking set dates: {e}")
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(1500)


    def uncheck_accommodation_option(self) -> None:
        """Uncheck the accommodation booking checkbox"""
        logger.info("Looking for accommodation checkbox")
        
        try:
            self.page.wait_for_timeout(1000)
            
            # Strategy 1: Direct checkbox selectors
            checkbox_selectors = [
                "[data-test='accommodationCheckbox']",
                "[data-test='BookingCheckbox']",
                "input[type='checkbox'][name*='accommodation']",
                "input[type='checkbox'][name*='booking']"
            ]
            
            for selector in checkbox_selectors:
                try:
                    logger.info(f"Trying checkbox selector: {selector}")
                    if self.is_visible(selector, timeout=2000):
                        # Check if it's checked
                        is_checked = self.page.is_checked(selector)
                        logger.info(f"Checkbox state: {'checked' if is_checked else 'unchecked'}")
                        
                        if is_checked:
                            self.page.uncheck(selector)
                            logger.info(f"✓ Unchecked accommodation: {selector}")
                        else:
                            logger.info("Accommodation already unchecked")
                        return
                except Exception as e:
                    logger.debug(f"Checkbox selector {selector} failed: {e}")
                    continue
            
            # Strategy 2: Find by label text and click it
            label_selectors = [
                "label:has-text('accommodation')",
                "label:has-text('Booking.com')",
                "div:has-text('accommodation with Booking.com')"
            ]
            
            for selector in label_selectors:
                try:
                    logger.info(f"Trying label selector: {selector}")
                    if self.is_visible(selector, timeout=2000):
                        # Check if associated checkbox is checked
                        label_element = self.page.locator(selector).first
                        
                        # Find checkbox near this label
                        checkbox = label_element.locator("..").locator("input[type='checkbox']").first
                        
                        if checkbox.is_visible():
                            is_checked = checkbox.is_checked()
                            logger.info(f"Found checkbox via label, checked: {is_checked}")
                            
                            if is_checked:
                                label_element.click()
                                logger.info(f"✓ Clicked label to uncheck: {selector}")
                            else:
                                logger.info("Checkbox already unchecked (via label)")
                            return
                except Exception as e:
                    logger.debug(f"Label selector {selector} failed: {e}")
                    continue
            
            # Strategy 3: Find by data-test attribute containing "accommodation"
            try:
                accommodation_section = self.page.locator("[data-test*='ccommodation']").first
                if accommodation_section.is_visible(timeout=2000):
                    logger.info("Found accommodation section")
                    
                    # Look for checkbox within this section
                    checkbox = accommodation_section.locator("input[type='checkbox']").first
                    
                    if checkbox.is_visible():
                        is_checked = checkbox.is_checked()
                        if is_checked:
                            checkbox.uncheck()
                            logger.info("✓ Unchecked accommodation via section")
                        else:
                            logger.info("Accommodation already unchecked (via section)")
                        return
            except Exception as e:
                logger.debug(f"Section strategy failed: {e}")
            
            logger.warning("Could not find accommodation checkbox - it may not exist or already be unchecked")
            
        except Exception as e:
            logger.warning(f"Error with accommodation checkbox: {e}")
    
    def click_search_button(self) -> None:
        """Click the search button to submit the search"""
        logger.info("Clicking search button")
        
        try:
            self.page.wait_for_timeout(1000)
            
            search_selectors = [
                "[data-test='LandingSearchButton']",
                "button[type='submit']",
                "button:has-text('Search')",
                "[data-test='SearchButton']",
                "button:has-text('Search flights')"
            ]
            
            for selector in search_selectors:
                try:
                    if self.is_visible(selector, timeout=2000):
                        logger.info(f"Found search button: {selector}")
                        self.click(selector)
                        logger.info("✓ Search button clicked")
                        self.page.wait_for_timeout(3000)
                        return
                except Exception:
                    continue
            
            logger.error("Could not find search button")
            
        except Exception as e:
            logger.error(f"Error clicking search button: {e}")
    
    def verify_redirected_to_results(self) -> bool:
        """
        Verify user is redirected to search results page
        
        Returns:
            True if redirected to results page
        """
        try:
            logger.info("Verifying redirect to search results...")
            
            # Wait for URL to change
            self.page.wait_for_timeout(5000)
            current_url = self.get_current_url()
            logger.info(f"Current URL: {current_url}")
            
            # Check if URL contains search/results indicators
            is_results_page = any(keyword in current_url.lower() for keyword in ['search', 'results', 'booking'])
            
            if is_results_page:
                logger.info("✓ Successfully redirected to search results page")
            else:
                logger.warning(f"URL does not appear to be results page: {current_url}")
            
            return is_results_page
            
        except Exception as e:
            logger.error(f"Error verifying redirect: {e}")
            return False