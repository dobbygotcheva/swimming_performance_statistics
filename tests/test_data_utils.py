import unittest
import os
import tempfile
from webapp import data_utils

class TestDataUtils(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.original_get_base_dir = data_utils.get_base_dir
        data_utils.get_base_dir = lambda: self.test_dir
        
        # Create some test data files
        os.makedirs(os.path.join(self.test_dir, 'swimdata2', 'swimdata2'), exist_ok=True)
        
        # Create a test swimmer file
        test_file = os.path.join(self.test_dir, 'swimdata2', 'swimdata2', 'John-10-100m-Freestyle.txt')
        with open(test_file, 'w') as f:
            f.write('1:30.00,1:31.00,1:29.50\n')
        
        # Create a test date file
        test_date_file = os.path.join(self.test_dir, 'swimdata2', 'swimdata2', '2024-01-01.txt')
        with open(test_date_file, 'w') as f:
            f.write('John\nJane\n')

    def tearDown(self):
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
        # Restore original get_base_dir function
        data_utils.get_base_dir = self.original_get_base_dir

    def test_get_all_available_dates(self):
        """Test getting all available dates"""
        dates = data_utils.get_all_available_dates()
        self.assertIn('2024-01-01', dates)

    def test_get_swimmers_for_date(self):
        """Test getting swimmers for a specific date"""
        swimmers = data_utils.get_swimmers_for_date('2024-01-01')
        self.assertIn('John', swimmers)
        self.assertIn('Jane', swimmers)

    def test_get_swimmer_age(self):
        """Test getting a swimmer's age for an event"""
        age = data_utils.get_swimmer_age('John', '100', 'Freestyle')
        self.assertEqual(age, '10')

    def test_get_swimmers_times(self):
        """Test getting a swimmer's times for an event"""
        times = data_utils.get_swimmers_times('John', '10', '100', 'Freestyle', '2024-01-01')
        self.assertEqual(len(times), 3)
        self.assertEqual(times[0][0], '1:30.00')
        self.assertEqual(times[1][0], '1:31.00')
        self.assertEqual(times[2][0], '1:29.50')

    def test_get_events_for_swimmer_date(self):
        """Test getting events for a swimmer on a specific date"""
        events = data_utils.get_events_for_swimmer_date('John', '2024-01-01')
        self.assertIn('100m Freestyle', events)

if __name__ == '__main__':
    unittest.main() 