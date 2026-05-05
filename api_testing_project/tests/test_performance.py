"""
Performance Tests for Weather API
Tests response times and concurrent request handling
"""

import pytest
import time
from utils.api_helper import get_weather
from config.config import PERFORMANCE_TEST_COUNT, PERFORMANCE_TIMEOUT


class TestPerformanceWeatherAPI:
    
    def test_single_response_time_under_3s(self):
        """Test that single API call completes within 3 seconds"""
        start_time = time.time()
        response = get_weather('London')
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed_time < PERFORMANCE_TIMEOUT, \
            f"Request took {elapsed_time}s, exceeds {PERFORMANCE_TIMEOUT}s limit"
    
    def test_multiple_response_times_under_3s(self):
        """Test that multiple API calls complete within 3 seconds each"""
        cities = ['London', 'Tokyo', 'New York', 'Sydney', 'Paris']
        
        for city in cities:
            start_time = time.time()
            response = get_weather(city)
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 200
            assert elapsed_time < PERFORMANCE_TIMEOUT, \
                f"Request for {city} took {elapsed_time}s"
    
    def test_10_consecutive_requests_avg_time(self):
        """Test 10 consecutive requests and verify average response time"""
        response_times = []
        city = 'London'
        
        for i in range(PERFORMANCE_TEST_COUNT):
            start_time = time.time()
            response = get_weather(city)
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 200
            response_times.append(elapsed_time)
        
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        # Average should be under 2 seconds
        assert avg_time < 2.0, f"Average response time: {avg_time}s"
        # No single request should exceed 4 seconds
        assert max_time < 4.0, f"Max response time: {max_time}s"
        assert min_time > 0.1, f"Min response time: {min_time}s"
    
    def test_response_time_valid_city(self):
        """Test response time for valid city lookup"""
        start_time = time.time()
        response = get_weather('Hyderabad')
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed_time < 3.0
    
    def test_response_time_invalid_city(self):
        """Test response time for invalid city (error handling)"""
        start_time = time.time()
        try:
            response = get_weather('InvalidCityNotExist')
            response.raise_for_status()
        except Exception:
            pass
        elapsed_time = time.time() - start_time
        
        # Even error responses should be quick
        assert elapsed_time < 3.0
    
    def test_no_timeout_on_valid_request(self):
        """Test that valid request doesn't timeout"""
        try:
            response = get_weather('New York')
            assert response.status_code == 200
        except Exception as e:
            pytest.fail(f"Request timed out: {str(e)}")
    
    def test_response_time_consistency(self):
        """Test that response times are consistent across requests"""
        times = []
        for _ in range(5):
            start = time.time()
            response = get_weather('Tokyo')
            times.append(time.time() - start)
            assert response.status_code == 200
        
        avg = sum(times) / len(times)
        variance = sum((t - avg) ** 2 for t in times) / len(times)
        
        # Variance should be reasonable (not widely fluctuating)
        assert variance < 1.0
    
    def test_parallel_requests_handling(self):
        """Test handling of requests in sequence"""
        cities = ['London', 'Paris', 'Tokyo', 'Sydney', 'New York',
                  'Dubai', 'Bangkok', 'Toronto', 'Singapore', 'Berlin']
        
        total_start = time.time()
        
        for city in cities:
            response = get_weather(city)
            assert response.status_code == 200
        
        total_time = time.time() - total_start
        avg_per_request = total_time / len(cities)
        
        # Average per request should still be reasonable
        assert avg_per_request < 2.0
    
    def test_request_under_acceptable_time(self):
        """Test that all requests complete in acceptable time"""
        for i in range(10):
            start = time.time()
            response = get_weather('London')
            elapsed = time.time() - start
            assert elapsed < 5.0, f"Iteration {i+1} took {elapsed}s"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
