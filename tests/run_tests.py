import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all test modules
from tests.test_routes import TestRoutes
from tests.test_data_utils import TestDataUtils
from tests.test_convert_utils import TestConvertUtils

def run_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestRoutes))
    test_suite.addTest(unittest.makeSuite(TestDataUtils))
    test_suite.addTest(unittest.makeSuite(TestConvertUtils))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return 0 if all tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 