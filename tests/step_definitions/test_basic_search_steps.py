"""
Step definitions for basic search feature
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pages.home_page import HomePage
from playwright.sync_api import Page
import logging

logger = logging.getLogger(__name__)

# Load scenarios from feature file
scenarios('../features/basic_search.feature')


@pytest.fixture
def homepage(page: Page) -> HomePage:
    """
    Fixture to create HomePage instance
    
    Args:
        page: Playwright page fixture
        
    Returns:
        HomePage instance
    """
    return HomePage(page)


@given(parsers.parse('As an not logged user navigate to homepage {url}'))
@given('As an not logged user navigate to homepage https://www.kiwi.com/en/')
def navigate_to_homepage(homepage: HomePage, url: str = "https://www.kiwi.com/en/"):
    """
    Navigate to Kiwi.com homepage
    
    Args:
        homepage: HomePage instance
        url: URL to navigate to
    """
    logger.info(f"Step: Navigate to homepage - {url}")
    homepage.open()
    assert homepage.get_current_url() == url or url in homepage.get_current_url(), \
        f"Failed to navigate to {url}"


@when('I select one-way trip type')
def select_one_way_trip(homepage: HomePage):
    """
    Select one-way trip type
    
    Args:
        homepage: HomePage instance
    """
    logger.info("Step: Select one-way trip type")
    homepage.select_trip_type('one-way')


@when(parsers.parse('Set as departure airport {airport_code}'))
def set_departure_airport(homepage: HomePage, airport_code: str):
    """
    Set departure airport
    
    Args:
        homepage: HomePage instance
        airport_code: Airport code (e.g., RTM)
    """
    logger.info(f"Step: Set departure airport - {airport_code}")
    homepage.set_departure_airport(airport_code)


@when(parsers.parse('Set the arrival Airport {airport_code}'))
def set_arrival_airport(homepage: HomePage, airport_code: str):
    """
    Set arrival airport
    
    Args:
        homepage: HomePage instance
        airport_code: Airport code (e.g., MAD)
    """
    logger.info(f"Step: Set arrival airport - {airport_code}")
    homepage.set_arrival_airport(airport_code)


@when(parsers.parse('Set the departure time {weeks:d} week in the future starting current date'))
@when('Set the departure time 1 week in the future starting current date')
def set_departure_date(homepage: HomePage, weeks: int = 1):
    """
    Set departure date weeks in the future
    
    Args:
        homepage: HomePage instance
        weeks: Number of weeks from now
    """
    logger.info(f"Step: Set departure date - {weeks} week(s) from now")
    homepage.set_departure_date(weeks_from_now=weeks)


@when(parsers.parse('Uncheck the "{option}" option'))
@when('Uncheck the "Check accommodation with booking.com" option')
def uncheck_accommodation(homepage: HomePage, option: str = None):
    """
    Uncheck accommodation option
    
    Args:
        homepage: HomePage instance
        option: Option text (not used in implementation)
    """
    logger.info(f"Step: Uncheck accommodation option")
    homepage.uncheck_accommodation_option()


@when('Click the search button')
def click_search(homepage: HomePage):
    """
    Click search button
    
    Args:
        homepage: HomePage instance
    """
    logger.info("Step: Click search button")
    homepage.click_search_button()


@then('I am redirected to search results page')
def verify_results_page(homepage: HomePage):
    """
    Verify redirection to search results page
    
    Args:
        homepage: HomePage instance
    """
    logger.info("Step: Verify redirect to results page")
    is_redirected = homepage.verify_redirected_to_results()
    assert is_redirected, "Failed to redirect to search results page"
    logger.info("Successfully verified redirect to search results page")