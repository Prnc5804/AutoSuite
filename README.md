# Capstone Assignment 2: Selenium Python Framework Development

## Objective
A robust Selenium Python Automation Framework using **Unittest**, **PyTest**, **Page Object Model (POM)**, Utility Classes, Configuration Management, CSV Test Data Handling, Screenshots on Failure, and HTML Reporting.

## Application Under Test
**TutorialsNinja Demo Store**: https://tutorialsninja.com/demo/

## Project Structure

```
wiproProject/
├── config/
│   └── config.ini                  # Central configuration (URL, browser, credentials, paths)
├── pages/
│   ├── __init__.py
│   ├── base_page.py                # Base Page (common Selenium methods)
│   ├── home_page.py                # Home Page Object
│   ├── login_page.py               # Login Page Object
│   ├── my_account_page.py          # My Account Page Object
│   └── search_results_page.py      # Search Results Page Object
├── tests/
│   ├── __init__.py
│   ├── test_login.py               # Login Tests (Unittest)
│   ├── test_search.py              # Search Tests (Unittest)
│   ├── test_login_pytest.py        # Login Tests (PyTest)
│   └── test_search_pytest.py       # Search Tests (PyTest)
├── utilities/
│   ├── __init__.py
│   ├── read_config.py              # Configuration Reader (configparser)
│   ├── csv_reader.py               # CSV Test Data Reader
│   ├── custom_logger.py            # Custom Logger (file + console)
│   └── screenshot_util.py          # Screenshot Capture Utility
├── test_data/
│   ├── login_data.csv              # Login test data (data-driven)
│   └── search_data.csv             # Search test data (data-driven)
├── screenshots/                    # Auto-captured failure screenshots
├── reports/                        # Generated HTML/text reports
├── logs/                           # Execution log files
├── conftest.py                     # PyTest fixtures and hooks
├── pytest.ini                      # PyTest configuration
├── run_unittest.py                 # Unittest runner script
├── run_pytest.py                   # PyTest runner script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Setup Instructions

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```


### 2. Register a Test Account (One-time)
Before running login tests, register a test account at:
https://tutorialsninja.com/demo/index.php?route=account/register

Use the email/password configured in `.env`.

## How to Run Tests

### Run All Unittest Tests
```bash
python run_unittest.py
```

### Run All PyTest Tests (with HTML Report)
```bash
python run_pytest.py
```

### Run PyTest by Marker
```bash
python run_pytest.py smoke
python run_pytest.py regression
python run_pytest.py login
python run_pytest.py search
```

### Run PyTest Directly
```bash
# All pytest tests with HTML report
pytest tests/test_login_pytest.py tests/test_search_pytest.py -v --html=reports/report.html --self-contained-html

# Only smoke tests
pytest tests/ -v -m smoke --html=reports/smoke_report.html --self-contained-html

# Only login tests
pytest tests/ -v -m login

# Only search tests
pytest tests/ -v -m search
```

### Run Individual Unittest Files
```bash
python -m unittest tests.test_login -v
python -m unittest tests.test_search -v
```

## Framework Features

| Feature | Implementation |
|---|---|
| **Unittest** | `test_login.py`, `test_search.py` |
| **PyTest** | `test_login_pytest.py`, `test_search_pytest.py` |
| **Page Object Model** | `pages/` package (BasePage → HomePage, LoginPage, etc.) |
| **Utility Classes** | `utilities/` (ReadConfig, CSVReader, CustomLogger, ScreenshotUtil) |
| **Configuration Management** | `config/config.ini` via `configparser` |
| **Test Data Handling (CSV)** | `test_data/*.csv` via `csv_reader.py` + `@pytest.mark.parametrize` |
| **Screenshots on Failure** | Auto-capture via `tearDown()` and `pytest_runtest_makereport` hook |
| **HTML Reporting** | `pytest-html` for PyTest; text reports for Unittest |
| **Custom Markers** | `@pytest.mark.smoke`, `regression`, `login`, `search`, `data_driven` |
| **Logging** | File + console logging via `custom_logger.py` |

## Test Coverage

### Login Tests (6 test cases + 5 data-driven)
| Test ID | Description | Type |
|---|---|---|
| TC_LG_001 | Valid login credentials | Smoke |
| TC_LG_002 | Invalid email and password | Regression |
| TC_LG_003 | Empty email field | Regression |
| TC_LG_004 | Empty password field | Regression |
| TC_LG_005 | Both fields empty | Regression |
| TC_LG_006 | Login page title verification | Smoke |
| CSV-driven | 5 rows from `login_data.csv` | Data-Driven |

### Search Tests (7 test cases + 5 data-driven)
| Test ID | Description | Type |
|---|---|---|
| TC_SR_001 | Search for 'MacBook' | Smoke |
| TC_SR_002 | Search for 'iMac' | Smoke |
| TC_SR_003 | Search for 'iPhone' | Regression |
| TC_SR_004 | Search for non-existent product | Regression |
| TC_SR_005 | Search with empty query | Regression |
| TC_SR_006 | Search results page title | Smoke |
| TC_SR_007 | Product count verification | Regression |
| CSV-driven | 5 rows from `search_data.csv` | Data-Driven |

## Author
**Prince** — Capstone Assignment 2
