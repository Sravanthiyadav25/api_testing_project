"""
Unit Tests for Weather API
Tests basic API response structure and required fields
"""

import pytest
import json
from utils.api_helper import get_weather, parse_weather_response
from config.config import VALID_CITIES, OPENWEATHERMAP_API_KEY


class TestUnitWeatherAPI:
    
    def test_response_status_code_valid_city(self):
        """Verify API returns 200 status code for valid city"""
        response = get_weather(VALID_CITIES[0])
        assert response.status_code == 200
    
    def test_response_contains_temperature(self):
        """Verify response contains temperature field"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert 'main' in data
        assert 'temp' in data['main']
        assert isinstance(data['main']['temp'], (int, float))
    
    def test_response_contains_humidity(self):
        """Verify response contains humidity field"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert 'main' in data
        assert 'humidity' in data['main']
        assert 0 <= data['main']['humidity'] <= 100
    
    def test_response_contains_city_name(self):
        """Verify response contains city name field"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert 'name' in data
        assert isinstance(data['name'], str)
        assert len(data['name']) > 0
    
    def test_response_is_valid_json(self):
        """Verify API response is valid JSON"""
        response = get_weather(VALID_CITIES[0])
        try:
            data = response.json()
            assert isinstance(data, dict)
            assert 'main' in data
        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")
    
    def test_response_contains_weather_description(self):
        """Verify response contains weather description"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert 'weather' in data
        assert len(data['weather']) > 0
        assert 'description' in data['weather'][0]
    
    def test_response_contains_country_code(self):
        """Verify response contains country code"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert 'sys' in data
        assert 'country' in data['sys']
    
    def test_parse_response_returns_dict(self):
        """Verify response parsing returns dictionary"""
        response = get_weather(VALID_CITIES[0])
        parsed = parse_weather_response(response)
        assert isinstance(parsed, dict)
        assert 'city' in parsed
        assert 'temp' in parsed
        assert 'humidity' in parsed
    
    def test_temperature_is_numeric(self):
        """Verify temperature is a numeric value"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        temp = data['main']['temp']
        assert isinstance(temp, (int, float))
    
    def test_humidity_is_valid_percentage(self):
        """Verify humidity is between 0 and 100"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        humidity = data['main']['humidity']
        assert 0 <= humidity <= 100


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
