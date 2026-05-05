"""
Configuration module for Automated API Testing Dashboard
Contains API credentials, URLs, timeouts, and test data
"""

# ==================== API CONFIGURATION ====================
OPENWEATHERMAP_API_KEY = 'your_api_key_here'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
REQUEST_TIMEOUT = 10

# ==================== TEST DATA ====================
# Valid test cities
VALID_CITIES = [
    'Hyderabad',
    'London',
    'New York',
    'Tokyo',
    'Sydney'
]

# Invalid test inputs
INVALID_CITIES = [
    'InvalidCityXYZ123',
    '12345',
    'xxxxxxxxxxxxxx',
    ''
]

# Edge case test inputs
EDGE_CASE_CITIES = [
    'São Paulo',
    'LONDON',
    'london',
    'New York',
    'Los Angeles'
]

# Performance test settings
PERFORMANCE_TEST_COUNT = 10
PERFORMANCE_TIMEOUT = 3  # seconds

# Flask app settings
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Report settings
REPORT_FOLDER = 'reports'
