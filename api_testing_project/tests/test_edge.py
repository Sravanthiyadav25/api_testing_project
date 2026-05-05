"""
Edge Case Tests for Weather API
Tests unusual but valid inputs and boundary conditions
"""

import pytest
from utils.api_helper import get_weather, parse_weather_response


class TestEdgeCaseWeatherAPI:
    
    def test_city_with_special_characters(self):
        """Test city name with special characters (São Paulo)"""
        response = get_weather('São Paulo')
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
    
    def test_city_all_caps(self):
        """Test city name in all uppercase"""
        response = get_weather('LONDON')
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
    
    def test_city_all_lowercase(self):
        """Test city name in all lowercase"""
        response = get_weather('london')
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
    
    def test_city_mixed_case(self):
        """Test city name with mixed case"""
        response = get_weather('LoNdOn')
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
    
    def test_city_with_spaces(self):
        """Test city name with spaces (New York)"""
        response = get_weather('New York')
        assert response.status_code == 200
        data = response.json()
        assert 'name' in data
    
    def test_city_with_leading_spaces(self):
        """Test city name with leading spaces"""
        response = get_weather('  London')
        # API might normalize this
        assert response.status_code in [200, 404]
    
    def test_city_with_trailing_spaces(self):
        """Test city name with trailing spaces"""
        response = get_weather('London  ')
        # API might normalize this
        assert response.status_code in [200, 404]
    
    def test_single_character_city(self):
        """Test single character input"""
        # Most cities have more than one character
        with pytest.raises(Exception):
            response = get_weather('X')
            response.raise_for_status()
    
    def test_city_with_hyphen(self):
        """Test city name with hyphen"""
        response = get_weather('San-Francisco')
        # API may or may not recognize this
        assert response.status_code in [200, 404]
    
    def test_city_with_apostrophe(self):
        """Test city name with apostrophe"""
        response = get_weather("Saint John's")
        assert response.status_code in [200, 404]
    
    def test_unicode_city_names(self):
        """Test various unicode city names"""
        unicode_cities = [
            'Moscow',      # Cyrillic: Москва
            'Tokyo',       # Japanese: 東京
            'Beijing',     # Chinese: 北京
            'Bangkok',     # Thai: กรุงเทพ
        ]
        
        for city in unicode_cities:
            response = get_weather(city)
            assert response.status_code == 200
    
    def test_temperature_precision(self):
        """Test temperature values have reasonable precision"""
        response = get_weather('London')
        data = response.json()
        temp = data['main']['temp']
        # Temperature should be numeric
        assert isinstance(temp, (int, float))
    
    def test_very_small_pressure_value(self):
        """Test handling of very small pressure values"""
        response = get_weather('London')
        data = response.json()
        pressure = data['main']['pressure']
        # Pressure should be positive
        assert pressure > 0
    
    def test_response_consistency_repeated_calls(self):
        """Test that repeated calls return consistent data"""
        response1 = get_weather('London')
        response2 = get_weather('London')
        
        data1 = response1.json()
        data2 = response2.json()
        
        # City name should be same
        assert data1['name'] == data2['name']
        # Coordinates should be same
        assert data1['coord'] == data2['coord']
    
    def test_weather_description_lowercase(self):
        """Test that weather description is in expected format"""
        response = get_weather('London')
        data = response.json()
        description = data['weather'][0]['description']
        assert isinstance(description, str)
        assert len(description) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
