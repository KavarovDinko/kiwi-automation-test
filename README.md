# Kiwi.com Test Automation Framework

Python-based automation testing framework for Kiwi.com flight search functionality using Playwright and pytest-bdd.

## Overview

This project automates the testing of Kiwi.com's flight search feature, specifically focusing on one-way flight searches. The framework follows Page Object Model (POM) design pattern and uses Behavior-Driven Development (BDD) approach with Gherkin syntax.

## Tech Stack

- **Python 3.10+** - Programming language
- **Playwright** - Browser automation
- **pytest** - Testing framework
- **pytest-bdd** - BDD support with Gherkin
- **pytest-html** - HTML test reports

## Project Structure

```
kiwi-automation-test/
├── pages/                          # Page Object Models
│   ├── base_page.py               # Base page with common methods
│   └── homepage.py                # Kiwi.com homepage POM
├── tests/
│   ├── features/                  # Gherkin feature files
│   │   └── basic_search.feature
│   ├── step_definitions/          # Step implementations
│   │   └── test_basic_search_steps.py
│   └── conftest.py                # pytest configuration
├── reports/                       # Test reports and screenshots
├── .github/workflows/             # CI/CD workflows
├── Dockerfile                     # Container configuration
├── docker-compose.yml             # Docker services
├── pytest.ini                     # pytest settings
└── requirements.txt               # Python dependencies
```

## Setup

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd kiwi-automation-test
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

## Running Tests

### Local Execution

```bash
# Run all tests
pytest -v

# Run with browser visible
pytest -v --headed

# Run specific test
pytest -v -m "basic_search and one_way"

# Run with HTML report
pytest -v --html=reports/report.html --self-contained-html

# Run with slow motion (for debugging)
pytest -v --headed --slowmo=1000
```

### Using Docker

```bash
# Build and run tests
docker-compose up --build

# Run specific test suite
docker-compose --profile t1 up t1-test

# Clean up
docker-compose down
```

### Test Markers

Tests are organized using pytest markers:

- `@basic_search` - Basic search functionality tests
- `@one_way` - One-way flight tests  
- `@smoke` - Critical path smoke tests

Example:
```bash
pytest -v -m smoke  # Run only smoke tests
```

## Test Coverage

### T1 - One Way Flight Search

**Scenario**: User searches for a one-way flight from Rotterdam (RTM) to Madrid (MAD) departing 1 week from current date.

**Steps**:
1. Navigate to Kiwi.com homepage
2. Select one-way trip type
3. Enter departure airport (RTM)
4. Enter arrival airport (MAD)
5. Select departure date (1 week from today)
6. Uncheck accommodation option
7. Click search button
8. Verify redirect to results page

## CI/CD

### GitHub Actions

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Daily schedule (8 AM UTC)
- Manual trigger via workflow_dispatch

View workflow runs in the **Actions** tab of the repository.

### Artifacts

- HTML test reports
- Screenshots on failure
- 30-day retention

## Configuration

### Browser Selection

Tests support multiple browsers:

```bash
pytest --browser chromium  # Default
pytest --browser firefox
pytest --browser webkit
```

### Headless Mode

```bash
pytest --headed          # Show browser (default for local)
pytest --headed=False    # Headless (default for CI)
```

### Timeouts

Default timeouts are configured in `pages/base_page.py`:
- Element wait: 30 seconds
- Page load: 30 seconds

Adjust in `BasePage.__init__()` if needed.

## Debugging

### Screenshots on Failure

Screenshots are automatically captured on test failure:
```
reports/screenshots/<test_name>_<timestamp>.png
```

### Verbose Logging

Enable detailed logs:
```bash
pytest -v -s  # -s shows print statements and logs
```

### Playwright Inspector

Debug tests interactively:
```bash
PWDEBUG=1 pytest -v -m "basic_search and one_way"
```

## Key Features

- **POM Architecture** - Maintainable and reusable page objects
- **BDD Approach** - Business-readable test scenarios
- **Multiple Strategies** - Robust selector fallbacks for reliability
- **Auto Screenshots** - Failure diagnosis made easy
- **Docker Support** - Consistent execution environment
- **CI/CD Ready** - Automated testing in GitHub Actions

## Known Issues & Limitations

- Date picker requires specific class matching for Kiwi.com's dynamic UI
- Tests depend on stable internet connection for page loads

## Contributing

1. Create feature branch from `develop`
2. Write tests following existing patterns
3. Ensure tests pass locally
4. Submit pull request with description

## Troubleshooting

**Tests not discovered:**
```bash
pytest --collect-only  # Check test discovery
```

**Selector not found:**
- Check `reports/screenshots/` for failure screenshots
- Use `--headed --slowmo=2000` to watch test execution
- Verify element exists in browser DevTools

**Docker issues:**
```bash
docker system prune -a  # Clean Docker cache
docker-compose build --no-cache
```

## Contact
dinko.kavarov@gmail.com
For questions or issues, please open a GitHub issue in the repository.