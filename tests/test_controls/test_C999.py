"""
Tests for the C999 control.
"""
import os
import sys
import unittest
from tempfile import NamedTemporaryFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.business_controls_framework.controls.C999.control import C999Control


class TestC999Control(unittest.TestCase):
    """Tests for the C999 control."""
    
    def test_passing_case(self):
        """Test a case where the control should pass."""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("id,account_balance\n1,1\n2,999999\n")
            temp_file = f.name
        
        try:
            control = C999Control(data_file=temp_file)
            result = control.run()
            
            self.assertTrue(result.passed)
            self.assertEqual(result.control_id, "C999")
        finally:
            os.unlink(temp_file)
    
    def test_failing_case(self):
        """Test a case where the control should fail."""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("id,account_balance\n1,-1\n2,1000001\n")
            temp_file = f.name
        
        try:
            control = C999Control(data_file=temp_file)
            result = control.run()
            
            self.assertFalse(result.passed)
            self.assertEqual(result.control_id, "C999")
        finally:
            os.unlink(temp_file)
