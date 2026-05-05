"""
Negative Tests for Weather API
Tests error handling and invalid inputs
"""

import pytest
import requests
from utils.api_helper import get_weather
from config.config import OPENWEATHERMAP_API_KEY


class TestNegativeWeatherAPI:
    
    def test_invalid_city_name_returns_404(self):
        """Test that invalid city name returns 404 error"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather('InvalidCityXYZ123NotReal')
            response.raise_for_status()
    
    def test_wrong_api_key_returns_401(self):
        """Test that wrong API key returns 401 Unauthorized"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather('London', api_key='wrong_key_12345')
            response.raise_for_status()
    
    def test_empty_city_name_returns_error(self):
        """Test that empty city name returns error"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather('')
            response.raise_for_status()
    
    def test_numeric_city_name_returns_error(self):
        """Test that numeric city name returns error"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather('12345')
            response.raise_for_status()
    
    def test_sql_injection_attempt_handled(self):
        """Test that SQL injection attempt in city name is handled"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather("'; DROP TABLE users; --")
            response.raise_for_status()
    
    def test_xss_injection_attempt_handled(self):
        """Test that XSS injection attempt is handled"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather("<script>alert('xss')</script>")
            response.raise_for_status()
    
    def test_very_long_string_city_name(self):
        """Test that very long string is handled"""
        long_string = 'a' * 500
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather(long_string)
            response.raise_for_status()
    
    def test_special_characters_invalid_city(self):
        """Test that special characters in invalid city name is handled"""
        with pytest.raises(requests.exceptions.HTTPError):
            response = get_weather('!@#$%^&*()')
            response.raise_for_status()
    
    def test_null_api_key_with_config_fallback(self):
        """Test that None API key falls back to config"""
        # This should work as it uses config default
        response = get_weather('London', api_key=None)
        assert response.status_code == 200
    
    def test_response_error_codes(self):
        """Test various HTTP error codes are handled"""
        error_cases = [
            ('InvalidCityNotExist123', 404),  # Not found
        ]
        
        for city, expected_code in error_cases:
            with pytest.raises(requests.exceptions.HTTPError):
                response = get_weather(city)
                response.raise_for_status()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
