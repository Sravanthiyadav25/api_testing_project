"""
API Helper Module - Reusable functions for API interactions
Handles weather API calls with proper error handling and response parsing
"""

import requests
from config.config import BASE_URL, OPENWEATHERMAP_API_KEY, REQUEST_TIMEOUT


def get_weather(city, api_key=None):
    """
    Fetch weather data for a given city
    
    Args:
        city (str): City name to fetch weather for
        api_key (str): OpenWeatherMap API key (optional, uses config if None)
    
    Returns:
        requests.Response: Response object from API call
    
    Raises:
        requests.RequestException: If API call fails
    """
    if api_key is None:
        api_key = OPENWEATHERMAP_API_KEY
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise e


def parse_weather_response(response):
    """
    Parse weather API response into structured data
    
    Args:
        response (requests.Response): API response object
    
    Returns:
        dict: Parsed weather data with keys: city, temp, humidity, pressure, description
    """
    data = response.json()
    return {
        'city': data.get('name'),
        'temp': data.get('main', {}).get('temp'),
        'humidity': data.get('main', {}).get('humidity'),
        'pressure': data.get('main', {}).get('pressure'),
        'description': data.get('weather', [{}])[0].get('description'),
        'country': data.get('sys', {}).get('country')
    }
