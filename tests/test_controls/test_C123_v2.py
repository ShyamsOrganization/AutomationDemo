"""
Tests for the C123 V2 control.
"""
import os
import sys
import unittest
from tempfile import NamedTemporaryFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.business_controls_framework.controls.C123.control_v2 import C123ControlV2


class TestC123ControlV2(unittest.TestCase):
    """Tests for the C123 V2 control."""
    
    def test_passing_case(self):
        """Test a case where all bonuses are within the limit."""
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("name,salary,age,location,bonus\n")
            f.write("John Doe,100000,35,New York,15000\n")  # 15%
            f.write("Jane Smith,120000,42,San Francisco,20000\n")  # 16.7%
            f.write("Bob Johnson,80000,28,Chicago,12000\n")  # 15%
            temp_file = f.name
        
        try:
            control = C123ControlV2(temp_file)
            result = control.run()
            
            self.assertTrue(result.passed)
            self.assertEqual(result.control_id, "C123")
            self.assertEqual(len(result.reasons), 1)
            self.assertIn("within the maximum 20% limit", result.reasons[0])
        finally:
            os.unlink(temp_file)
    
    def test_failing_case(self):
        """Test a case where some bonuses exceed the limit."""
        with NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("name,salary,age,location,bonus\n")
            f.write("John Doe,100000,35,New York,15000\n")  # 15%
            f.write("Jane Smith,120000,42,San Francisco,25000\n")  # 20.8% - exceeds limit
            f.write("Bob Johnson,80000,28,Chicago,12000\n")  # 15%
            temp_file = f.name
        
        try:
            control = C123ControlV2(temp_file)
            result = control.run()
            
            self.assertFalse(result.passed)
            self.assertEqual(result.control_id, "C123")
            self.assertEqual(len(result.reasons), 1)
            self.assertIn("exceeds the maximum allowed 20%", result.reasons[0])
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()
