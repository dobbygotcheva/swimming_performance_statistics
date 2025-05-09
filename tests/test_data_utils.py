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

if __name__ == '__main__':
    unittest.main() 