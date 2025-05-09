import unittest
from webapp import convert_utils

class TestConvertUtils(unittest.TestCase):
    def test_time_to_seconds(self):
        """Test converting time strings to seconds"""
        test_cases = [
            ('1:30.00', 90.0),
            ('45.50', 45.5),
            ('2:15.75', 135.75),
            ('0:59.99', 59.99)
        ]
        
        for time_str, expected_seconds in test_cases:
            with self.subTest(time_str=time_str):
                self.assertEqual(convert_utils.time_to_seconds(time_str), expected_seconds)

    def test_seconds_to_time(self):
        """Test converting seconds to time strings"""
        test_cases = [
            (90.0, '1:30.00'),
            (45.5, '45.50'),
            (135.75, '2:15.75'),
            (59.99, '59.99')
        ]
        
        for seconds, expected_time in test_cases:
            with self.subTest(seconds=seconds):
                self.assertEqual(convert_utils.seconds_to_time(seconds), expected_time)

    def test_time_difference(self):
        """Test calculating time differences"""
        test_cases = [
            ('1:30.00', '1:31.00', '+1.00'),
            ('1:31.00', '1:30.00', '-1.00'),
            ('45.50', '45.00', '-0.50'),
            ('2:15.75', '2:15.00', '-0.75')
        ]
        
        for time1, time2, expected_diff in test_cases:
            with self.subTest(time1=time1, time2=time2):
                self.assertEqual(convert_utils.time_difference(time1, time2), expected_diff)

    def test_perform_conversions(self):
        """Test the main conversion function"""
        times = ['1:30.00', '1:31.00', '1:29.50']
        average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
        
        # Test average string format
        self.assertIsInstance(average_str, str)
        self.assertIn(':', average_str)
        
        # Test times are reversed (fastest to slowest)
        self.assertEqual(times_reversed[0], '1:29.50')  # Fastest
        self.assertEqual(times_reversed[-1], '1:31.00')  # Slowest
        
        # Test scaled times
        self.assertEqual(len(scaled), len(times))
        self.assertTrue(all(isinstance(t, float) for t in scaled))

if __name__ == '__main__':
    unittest.main() 