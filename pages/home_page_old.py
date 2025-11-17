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
                # trip_type_selectors = "[data-test='SearchFormModesPicker-active-return']"

                trip_types = "[data-test='ModePopupOption-oneWay']"
                
                for selector in trip_type_selectors:
                    try:
                        logger.info(f"Trying trip_type selector: {selector}")
                        if self.is_visible(selector, timeout=2000):
                            self.click(selector)
                            logger.info(f"✓ trip_type selected with: {selector}")
                            self.page.wait_for_timeout(500)
                            self.click(trip_types)
                            return
                    except Exception as e:
                        logger.debug(f"Selector {selector} failed: {e}")
                        continue

                # for selector in trip_types:
                #     try:
                #         logger.info(f"Trying to select one-way-trip with: {selector}")
                #         if self.is_visible(selector, timeout=2000):
                #             self.click(selector)
                #             logger.info(f"✓ One-way selected by: {selector}")
                #             self.page.wait_for_timeout(500)
                #             return
                #     except Exception as e:
                #         logger.debug(f"Selector {selector} failed: {e}")
                #         continue
                
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
                # "[data-test='SearchField-input'][data-test*='origin']",
                # "[data-test='PlacePickerInputPlace']:first-child input",
                # "input[placeholder*='From']",
                # "input[placeholder*='Where from']",
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
                        self.click(clear_departure_preselected_items)
                        self.page.wait_for_timeout(500)
                        self.page.fill(selector, "")
                        self.page.wait_for_timeout(300)
                        
                        # Type slowly (more reliable)
                        self.page.type(selector, airport_code, delay=100)
                        self.page.wait_for_timeout(1500)
                        
                        logger.info(f"✓ Typed {airport_code} in departure field")
                        
                        # Select from dropdown
                        # self._select_airport_from_dropdown(airport_code)
                        self.page.keyboard.press("Enter")
                        return
                        
                except Exception as e:
                    logger.debug(f"Departure selector {selector} failed: {e}")
                    continue
            
            logger.error("Could not find departure airport input field")
            
        except Exception as e:
            logger.error(f"Error setting departure airport: {e}")
            self.page.keyboard.press("Enter")
    
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
                        
                        # Select from dropdown
                        # self._select_airport_from_dropdown(airport_code)
                        self.page.keyboard.press("Enter")
                        return
                        
                except Exception as e:
                    logger.debug(f"Arrival selector {selector} failed: {e}")
                    continue
            
            logger.error("Could not find arrival airport input field")
            
        except Exception as e:
            logger.error(f"Error setting arrival airport: {e}")
    
    def _select_airport_from_dropdown(self, airport_code: str) -> None:
        """
        Select airport from dropdown suggestions
        
        Args:
            airport_code: Airport code to select
        """
        try:
            logger.info(f"Looking for dropdown with: {airport_code}")
            self.page.wait_for_timeout(1000)
            
            # Multiple dropdown selectors
            dropdown_selectors = [
                "[data-test='SearchPlaceField-origin']",
                f"[role='option']:has-text('{airport_code}')",
                f"li:has-text('{airport_code}')",
                f"div[class*='suggestion']:has-text('{airport_code}')",
                f"button:has-text('{airport_code}')"
            ]
            
            for selector in dropdown_selectors:
                try:
                    if self.is_visible(selector, timeout=2000):
                        logger.info(f"Found dropdown option: {selector}")
                        self.click(selector)
                        logger.info(f"✓ Selected {airport_code} from dropdown")
                        self.page.wait_for_timeout(500)
                        return
                except Exception:
                    continue
            
            # If no dropdown found, just press Enter
            logger.info("No dropdown found, pressing Enter")
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(500)
            
        except Exception as e:
            logger.warning(f"Dropdown selection issue: {e}")
            self.page.keyboard.press("Enter")
    
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
            "[data-test='SearchDateInput']",
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
        day = target_date.day
        month_number = target_date.month
        year = target_date.year
        date_string = target_date.strftime("%Y-%m-%d")
        
        logger.info(f"Looking for date: {day}/{month_number}/{year}")
        
        # Wait for calendar to appear
        self.page.wait_for_timeout(1500)
        
        # Strategy 1: Try data-date attribute
        try:
            date_selector = f"div[data-date='{date_string}']"
            if self.is_visible(date_selector, timeout=2000):
                logger.info(f"Found date by data-date: {date_selector}")
                self.click(date_selector)
                logger.info(f"✓ Selected date: {day}/{month_number}/{year}")
                self.page.wait_for_timeout(500)
                return
        except Exception as e:
            logger.debug(f"Strategy 1 failed: {e}")
        
        # Strategy 2: Try aria-label
        try:
            month_name = target_date.strftime("%B")
            aria_selector = f"div[aria-label*='{month_name} {day}']"
            if self.is_visible(aria_selector, timeout=2000):
                logger.info(f"Found date by aria-label: {aria_selector}")
                self.click(aria_selector)
                logger.info(f"✓ Selected date: {day}/{month_number}/{year}")
                self.page.wait_for_timeout(500)
                return
        except Exception as e:
            logger.debug(f"Strategy 2 failed: {e}")
        
        # Strategy 3: Find calendar day cells and click the matching one
        try:
            # Find all day cells in the calendar
            day_cells = self.page.locator("div[class*='CalendarDay']").all()
            logger.info(f"Found {len(day_cells)} calendar day cells")
            
            for cell in day_cells:
                cell_text = cell.inner_text().strip()
                if cell_text == str(day):
                    # Check if it's not disabled
                    if "disabled" not in cell.get_attribute("class").lower():
                        cell.click()
                        logger.info(f"✓ Clicked day cell: {day}")
                        self.page.wait_for_timeout(500)
                        return
        except Exception as e:
            logger.debug(f"Strategy 3 failed: {e}")
        
        # Strategy 4: Use keyboard navigation
        try:
            logger.info("Trying keyboard navigation for date")
            # Calculate days from today
            today = datetime.now()
            days_diff = (target_date - today).days
            
            if days_diff > 0 and days_diff < 60:  # Within 2 months
                for _ in range(days_diff):
                    self.page.keyboard.press("ArrowRight")
                    self.page.wait_for_timeout(100)
                
                self.page.keyboard.press("Enter")
                logger.info(f"✓ Selected date using keyboard: {days_diff} days from today")
                return
        except Exception as e:
            logger.debug(f"Strategy 4 failed: {e}")
        
        logger.warning("Could not select date from calendar")
        
    except Exception as e:
        logger.error(f"Error in calendar selection: {e}")
    
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