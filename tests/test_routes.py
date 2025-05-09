import unittest
from flask import url_for
from webapp import create_app
from webapp import data_utils, convert_utils

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_swimmers_route(self):
        """Test getting swimmers for a date"""
        # Mock the data_utils.get_swimmers_for_date function
        def mock_get_swimmers(date):
            return ['John', 'Jane'] if date == '2024-01-01' else []
        
        data_utils.get_swimmers_for_date = mock_get_swimmers
        
        response = self.client.get('/get_swimmers/2024-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['John', 'Jane'])

    def test_get_events_route(self):
        """Test getting events for a swimmer on a date"""
        # Mock the data_utils.get_events_for_swimmer_date function
        def mock_get_events(swimmer, date):
            return ['100m Freestyle', '200m Backstroke'] if swimmer == 'John' else []
        
        data_utils.get_events_for_swimmer_date = mock_get_events
        
        response = self.client.get('/get_events/John/2024-01-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['100m Freestyle', '200m Backstroke'])

    def test_show_bar_chart_route_invalid_data(self):
        """Test the show_bar_chart route with invalid data"""
        response = self.client.post('/showbarchart', data={
            'chosen_date': '',
            'swimmer': '',
            'event': ''
        })
        self.assertEqual(response.status_code, 302)  # Redirects back to index

    def test_time_conversion(self):
        """Test the time conversion utilities"""
        # Test time_to_seconds
        self.assertEqual(convert_utils.time_to_seconds('1:30.00'), 90.0)
        self.assertEqual(convert_utils.time_to_seconds('45.50'), 45.5)
        
        # Test seconds_to_time
        self.assertEqual(convert_utils.seconds_to_time(90.0), '1:30.00')
        self.assertEqual(convert_utils.seconds_to_time(45.5), '45.50')
        
        # Test time_difference
        self.assertEqual(convert_utils.time_difference('1:30.00', '1:31.00'), '+1.00')
        self.assertEqual(convert_utils.time_difference('1:31.00', '1:30.00'), '-1.00')

if __name__ == '__main__':
    unittest.main() 