"""
Tests for the C789 control.
"""
import os
import sys
import unittest
from tempfile import NamedTemporaryFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.business_controls_framework.controls.C789.control import C789Control


class TestC789Control(unittest.TestCase):
    """Tests for the C789 control."""
    
    def test_passing_case(self):
        """Test a case where the control should pass."""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("id,value\n")
            f.write("1,50\n")
            f.write("2,75\n")
            f.write("3,90\n")
            temp_file = f.name
        
        try:
            control = C789Control(data_file=temp_file)
            result = control.run()
            
            self.assertTrue(result.passed)
            self.assertEqual(result.control_id, "C789")
        finally:
            os.unlink(temp_file)
    
    def test_failing_case(self):
        """Test a case where the control should fail."""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("id,value\n")
            f.write("1,50\n")
            f.write("2,150\n")  # Exceeds threshold
            f.write("3,90\n")
            temp_file = f.name
        
        try:
            control = C789Control(data_file=temp_file)
            result = control.run()
            
            self.assertFalse(result.passed)
            self.assertEqual(result.control_id, "C789")
        finally:
            os.unlink(temp_file)
