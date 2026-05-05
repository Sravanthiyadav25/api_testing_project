"""
Functional Tests for Weather API
Tests complete workflows and data accuracy for valid cities
"""

import pytest
from utils.api_helper import get_weather, parse_weather_response
from config.config import VALID_CITIES


class TestFunctionalWeatherAPI:
    
    def test_valid_city_hyderabad(self):
        """Test weather data retrieval for Hyderabad"""
        response = get_weather('Hyderabad')
        assert response.status_code == 200
        data = response.json()
        assert data['name'].lower() == 'hyderabad'
    
    def test_valid_city_london(self):
        """Test weather data retrieval for London"""
        response = get_weather('London')
        assert response.status_code == 200
        data = response.json()
        assert 'London' in data['name']
    
    def test_valid_city_new_york(self):
        """Test weather data retrieval for New York"""
        response = get_weather('New York')
        assert response.status_code == 200
        data = response.json()
        assert 'New York' in data['name']
    
    def test_valid_city_tokyo(self):
        """Test weather data retrieval for Tokyo"""
        response = get_weather('Tokyo')
        assert response.status_code == 200
        data = response.json()
        assert 'Tokyo' in data['name']
    
    def test_temperature_in_realistic_range(self):
        """Verify temperature is in realistic global range (-50 to 60 Celsius)"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        temp = data['main']['temp']
        assert -50 <= temp <= 60
    
    def test_complete_weather_data_available(self):
        """Verify all essential weather data fields are present"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        
        required_fields = ['name', 'main', 'weather', 'sys']
        for field in required_fields:
            assert field in data
    
    def test_main_object_has_all_metrics(self):
        """Verify 'main' object contains all essential metrics"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        main = data['main']
        
        required_metrics = ['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity']
        for metric in required_metrics:
            assert metric in main
    
    def test_weather_array_not_empty(self):
        """Verify weather array contains at least one weather condition"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert len(data['weather']) > 0
        assert 'main' in data['weather'][0]
        assert 'description' in data['weather'][0]
    
    def test_pressure_value_is_valid(self):
        """Verify pressure value is in realistic range"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        pressure = data['main']['pressure']
        assert 800 <= pressure <= 1200  # Valid atmospheric pressure range
    
    def test_coord_object_present_and_valid(self):
        """Verify coordinates are present and valid"""
        response = get_weather(VALID_CITIES[0])
        data = response.json()
        assert 'coord' in data
        assert 'lon' in data['coord']
        assert 'lat' in data['coord']
        assert -90 <= data['coord']['lat'] <= 90
        assert -180 <= data['coord']['lon'] <= 180
    
    def test_multiple_cities_sequential_requests(self):
        """Test multiple sequential requests for different cities"""
        for city in VALID_CITIES[:3]:
            response = get_weather(city)
            assert response.status_code == 200
            data = response.json()
            assert 'name' in data
    
    def test_response_headers_valid(self):
        """Verify response headers are valid"""
        response = get_weather(VALID_CITIES[0])
        assert response.headers['Content-Type'].startswith('application/json')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
