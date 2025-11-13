@basic_search
Feature: Basic search form
    As a user
    I want to search for flights
    So that I can find travel options

    @one_way @smoke
    Scenario: T1 - One way flight search
        Given As an not logged user navigate to homepage https://www.kiwi.com/en/
        When I select one-way trip type
        And Set as departure airport RTM
        And Set the arrival Airport MAD
        And Set the departure time 1 week in the future starting current date
        And Uncheck the "Check accommodation with booking.com" option
        And Click the search button
        Then I am redirected to search results page