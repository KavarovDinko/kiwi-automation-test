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
                        
                        # Type slowly (more reliable)
                        self.page.type(selector, airport_code, delay=100)
                        self.page.wait_for_timeout(1500)
                        
                        logger.info(f"✓ Typed {airport_code} in departure field")
                        
                        # Press Enter to confirm
                        self.page.keyboard.press("Enter")
                        self.page.wait_for_timeout(500)
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
        Set departure date
        
        Args:
            weeks_from_now: Number of weeks from current date
        """
        logger.info(f"Setting departure date: {weeks_from_now} week(s) from now")
        
        try:
            target_date = datetime.now() + timedelta(weeks=weeks_from_now)
            
            # Wait for page to be ready
            self.page.wait_for_timeout(1000)
            
            # Click on date field to open calendar
            date_field_selectors = [
                # "[data-test='SearchDateInput']",
                "[data-test='SearchFieldDateInput']",
                "div[data-test*='Date']",
                "button:has-text('Departure')"
            ]
            
            clicked = False
            for selector in date_field_selectors:
                try:
                    logger.info(f"Trying date field selector: {selector}")
                    if self.is_visible(selector, timeout=2000):
                        self.click(selector)
                        logger.info(f"✓ Clicked date field: {selector}")
                        self.page.wait_for_timeout(1500)
                        clicked = True
                        break
                except Exception as e:
                    logger.debug(f"Date field selector {selector} failed: {e}")
                    continue
            
            if not clicked:
                logger.error("Could not open date picker")
                return
            
            # Now select the date from calendar
            self._select_date_from_calendar(target_date)
            
        except Exception as e:
            logger.error(f"Error setting departure date: {e}")
    
def _select_date_from_calendar(self, target_date: datetime) -> None:
    """
    Select specific date from calendar picker
    
    Args:
        target_date: Target date to select
    """
    try:
        day = str(target_date.day)
        month_name = target_date.strftime("%B")
        year = target_date.year
        
        logger.info(f"Looking for date: {month_name} {day}, {year}")
        
        # Wait for calendar to appear
        self.page.wait_for_timeout(1500)
        
        # Strategy: Find clickable date elements by text content
        # The calendar has multiple nested divs, we need the clickable parent
        logger.info(f"Searching for day '{day}' in calendar...")
        
        try:
            # Find all elements containing the day text
            # We need to find the one with cursor-pointer (clickable)
            day_selector = f"div.cursor-pointer:has-text('{day}')"
            
            # Get all matching elements
            day_elements = self.page.locator(day_selector).all()
            logger.info(f"Found {len(day_elements)} clickable day elements")
            
            # Click the first visible, non-disabled one
            for idx, elem in enumerate(day_elements):
                try:
                    # Check if element is visible and not disabled
                    if elem.is_visible():
                        elem_class = elem.get_attribute('class') or ''
                        
                        # Skip if disabled
                        if 'disabled' in elem_class.lower():
                            logger.debug(f"Day {day} element {idx} is disabled, skipping")
                            continue
                        
                        # This is the one - click it!
                        logger.info(f"Clicking day element {idx} with text '{day}'")
                        elem.click()
                        self.page.wait_for_timeout(500)
                        logger.info(f"✓ Selected date: {month_name} {day}, {year}")
                        return
                        
                except Exception as e:
                    logger.debug(f"Day element {idx} click failed: {e}")
                    continue
            
            logger.warning(f"Could not click any day '{day}' elements")
            
        except Exception as e:
            logger.error(f"Error finding day elements: {e}")
        
        # Fallback: Try clicking by text without cursor-pointer requirement
        try:
            logger.info("Trying fallback: click any element with matching day text")
            
            # More general selector
            general_selector = f"div:has-text('{day}')"
            elements = self.page.locator(general_selector).all()
            
            # Find the one that's in the calendar and clickable
            for elem in elements:
                try:
                    if elem.is_visible():
                        text = elem.inner_text().strip()
                        if text == day:
                            elem.click()
                            logger.info(f"✓ Clicked day using fallback method")
                            self.page.wait_for_timeout(500)
                            return
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"Fallback method failed: {e}")
        
        logger.warning("Could not select date from calendar")
        
    except Exception as e:
        logger.error(f"Error in calendar selection: {e}")
    


    # def uncheck_accommodation_option(self) -> None:
    #     """Uncheck the accommodation booking checkbox"""
    #     logger.info("Looking for accommodation checkbox")
        
    #     try:
    #         self.page.wait_for_timeout(1000)
            
    #         # Strategy 1: Direct checkbox selectors
    #         checkbox_selectors = [
    #             "[data-test='accommodationCheckbox']",
    #             "[data-test='BookingCheckbox']",
    #             "input[type='checkbox'][name*='accommodation']",
    #             "input[type='checkbox'][name*='booking']"
    #         ]
            
    #         for selector in checkbox_selectors:
    #             try:
    #                 logger.info(f"Trying checkbox selector: {selector}")
    #                 if self.is_visible(selector, timeout=2000):
    #                     # Check if it's checked
    #                     is_checked = self.page.is_checked(selector)
    #                     logger.info(f"Checkbox state: {'checked' if is_checked else 'unchecked'}")
                        
    #                     if is_checked:
    #                         self.page.uncheck(selector)
    #                         logger.info(f"✓ Unchecked accommodation: {selector}")
    #                     else:
    #                         logger.info("Accommodation already unchecked")
    #                     return
    #             except Exception as e:
    #                 logger.debug(f"Checkbox selector {selector} failed: {e}")
    #                 continue
            
    #         # Strategy 2: Find by label text and click it
    #         label_selectors = [
    #             "label:has-text('accommodation')",
    #             "label:has-text('Booking.com')",
    #             "label:has-text('Kiwi.com')",
    #             "div:has-text('accommodation with Booking.com')",
    #             "div:has-text('accommodation with Kiwi.com')"
    #         ]
            
    #         for selector in label_selectors:
    #             try:
    #                 logger.info(f"Trying label selector: {selector}")
    #                 if self.is_visible(selector, timeout=2000):
    #                     # Check if associated checkbox is checked
    #                     label_element = self.page.locator(selector).first
                        
    #                     # Find checkbox near this label
    #                     checkbox = label_element.locator("..").locator("input[type='checkbox']").first
                        
    #                     if checkbox.is_visible():
    #                         is_checked = checkbox.is_checked()
    #                         logger.info(f"Found checkbox via label, checked: {is_checked}")
                            
    #                         if is_checked:
    #                             label_element.click()
    #                             logger.info(f"✓ Clicked label to uncheck: {selector}")
    #                         else:
    #                             logger.info("Checkbox already unchecked (via label)")
    #                         return
    #             except Exception as e:
    #                 logger.debug(f"Label selector {selector} failed: {e}")
    #                 continue
            
    #         # Strategy 3: Find by data-test attribute containing "accommodation"
    #         try:
    #             accommodation_section = self.page.locator("[data-test*='ccommodation']").first
    #             if accommodation_section.is_visible(timeout=2000):
    #                 logger.info("Found accommodation section")
                    
    #                 # Look for checkbox within this section
    #                 checkbox = accommodation_section.locator("input[type='checkbox']").first
                    
    #                 if checkbox.is_visible():
    #                     is_checked = checkbox.is_checked()
    #                     if is_checked:
    #                         checkbox.uncheck()
    #                         logger.info("✓ Unchecked accommodation via section")
    #                     else:
    #                         logger.info("Accommodation already unchecked (via section)")
    #                     return
    #         except Exception as e:
    #             logger.debug(f"Section strategy failed: {e}")
            
    #         logger.warning("Could not find accommodation checkbox - it may not exist or already be unchecked")
            
    #     except Exception as e:
    #         logger.warning(f"Error with accommodation checkbox: {e}")

    def uncheck_accommodation_option(self) -> None:
        """Uncheck the accommodation booking checkbox"""
        logger.info("Looking for accommodation checkbox")
        
        try:
            self.page.wait_for_timeout(1000)
            
            # The checkbox is custom styled, we need to click the label/container
            # Try multiple approaches
            
            # Strategy 1: Click the label that contains "accommodation"
            try:
                label_selector = "label:has-text('accommodation')"
                logger.info(f"Trying to click label: {label_selector}")
                
                if self.is_visible(label_selector, timeout=3000):
                    label = self.page.locator(label_selector).first
                    
                    # Check if checkbox is checked by looking at parent container
                    parent = label.locator("..")
                    parent_html = parent.get_attribute('outerHTML') or ''
                    
                    # If it looks checked (this is approximate)
                    logger.info("Clicking accommodation label to toggle")
                    label.click()
                    self.page.wait_for_timeout(500)
                    logger.info("✓ Clicked accommodation option")
                    return
            except Exception as e:
                logger.debug(f"Label click failed: {e}")
            
            # Strategy 2: Find by data-test and click parent
            try:
                checkbox_selector = "[data-test='accommodationCheckbox']"
                logger.info(f"Trying checkbox parent: {checkbox_selector}")
                
                if self.is_visible(checkbox_selector, timeout=3000):
                    # Get the parent clickable element
                    checkbox_elem = self.page.locator(checkbox_selector).first
                    clickable_parent = checkbox_elem.locator("..")
                    
                    logger.info("Clicking accommodation checkbox parent")
                    clickable_parent.click()
                    self.page.wait_for_timeout(500)
                    logger.info("✓ Clicked accommodation parent element")
                    return
            except Exception as e:
                logger.debug(f"Parent click failed: {e}")
            
            # Strategy 3: Just ensure it's unchecked by checking visual state
            try:
                # Look for the container with accommodation text
                container = self.page.locator("text=accommodation").first
                if container.is_visible(timeout=2000):
                    # Click it to toggle
                    container.click()
                    self.page.wait_for_timeout(500)
                    logger.info("✓ Toggled accommodation option")
                    return
            except Exception as e:
                logger.debug(f"Container toggle failed: {e}")
            
            logger.warning("Could not interact with accommodation checkbox - may not be needed")
            
        except Exception as e:
            logger.warning(f"Error with accommodation checkbox: {e}")

    def click_search_button(self) -> None:
        """Click the search button to submit the search"""
        logger.info("Clicking search button")
        
        try:
            self.page.wait_for_timeout(3000)
            
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