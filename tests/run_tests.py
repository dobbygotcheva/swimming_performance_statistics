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
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRoutes))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDataUtils))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestConvertUtils))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print test results
    print("\nTest Results:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Return 0 if all tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 