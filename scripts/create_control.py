#!/usr/bin/env python3
"""
Control Creation Script

This script automates the creation of a new control directory with all required files.
"""
import os
import sys
import argparse
import shutil


def create_control_directory(control_id, description):
    """Create a new control directory with all required files."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    controls_dir = os.path.join(base_dir, 'src', 'business_controls_framework', 'controls')
    new_control_dir = os.path.join(controls_dir, control_id)
    data_dir = os.path.join(new_control_dir, 'data')
    
    os.makedirs(new_control_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(new_control_dir, '__init__.py'), 'w') as f:
        f.write(f'''"""
{control_id} Control Package

This package contains all components related to the {control_id} control.
"""
from .control import {control_id}Control
''')
    
    with open(os.path.join(data_dir, '__init__.py'), 'w') as f:
        f.write(f'''"""
Data files for {control_id} control.
"""
''')
    
    with open(os.path.join(new_control_dir, 'control.py'), 'w') as f:
        f.write(f'''"""
{control_id} Control Implementation

{description}
"""
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import CustomAssertion


class {control_id}Control(BaseControlV2):
    """
    {description}
    
    This control uses the CustomAssertion to verify data meets specific criteria.
    """
    
    def __init__(self, data_file, control_id="{control_id}", description="{description}"):
        """
        Initialize the control.
        
        Args:
            data_file: Path to the data file
            control_id: ID of the control
            description: Description of the control
        """
        super().__init__(control_id, description)
        self.data_file = data_file
    
    def create_query(self):
        """
        Create a query for this control.
        
        Returns:
            Query object
        """
        connector = CSVConnector(self.data_file)
        return SimpleQuery(connector)
    
    def create_assertion(self):
        """
        Create an assertion for this control.
        
        Returns:
            Assertion object
        """
        return CustomAssertion()
    
    def get_assertion_params(self):
        """
        Get parameters for the assertion.
        
        Returns:
            Dictionary of parameters
        """
        return {{
            "field": "value",
            "threshold": 100
        }}
''')
    
    with open(os.path.join(new_control_dir, 'assertion.py'), 'w') as f:
        f.write(f'''"""
Custom Assertion for {control_id}

This module provides a custom assertion implementation for the {control_id} control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class CustomAssertion(BaseAssertion):
    """Custom assertion implementation for {control_id} control."""
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the assertion against data.
        
        Args:
            data: Data to evaluate
            params: Parameters for the assertion
                
        Returns:
            Tuple of (passed, reasons)
        """
        field = params.get("field")
        threshold = params.get("threshold")
        
        if not all([field, threshold is not None]):
            return False, ["Missing required parameters for assertion"]
            
        results = data.get("results", [])
        passed = True
        reasons = []
        
        for item in results:
            value = item.get(field)
            
            if value is None:
                reasons.append(f"Missing field: {{field}}")
                passed = False
                continue
                
            if value > threshold:
                reasons.append(
                    f"Value {{value}} exceeds threshold {{threshold}}"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values meet the criteria")
            
        return passed, reasons
''')
    
    with open(os.path.join(new_control_dir, 'query.py'), 'w') as f:
        f.write(f'''"""
Simple Query for {control_id}

This module provides a simple query implementation for the {control_id} control.
"""
from typing import Dict, Any

from ...query_engine.base_query import BaseQuery


class SimpleQuery(BaseQuery):
    """Simple query implementation for {control_id} control."""
    
    def __init__(self, connector, query_string="all"):
        """
        Initialize a simple query.
        
        Args:
            connector: Data connector to use for executing queries
            query_string: Query string to execute
        """
        super().__init__(connector)
        self.query_string = query_string
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the query.
        
        Returns:
            Query results
        """
        results = self.connector.execute_query(self.query_string)
        return {{"results": results}}
''')
    
    test_dir = os.path.join(base_dir, 'tests', 'test_controls')
    with open(os.path.join(test_dir, f'test_{control_id}.py'), 'w') as f:
        f.write(f'''"""
Tests for the {control_id} control.
"""
import os
import sys
import unittest
from tempfile import NamedTemporaryFile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.business_controls_framework.controls.{control_id}.control import {control_id}Control


class Test{control_id}Control(unittest.TestCase):
    """Tests for the {control_id} control."""
    
    def test_passing_case(self):
        """Test a case where the control should pass."""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("id,value\\n")
            f.write("1,50\\n")
            f.write("2,75\\n")
            f.write("3,90\\n")
            temp_file = f.name
        
        try:
            control = {control_id}Control(data_file=temp_file)
            result = control.run()
            
            self.assertTrue(result.passed)
            self.assertEqual(result.control_id, "{control_id}")
        finally:
            os.unlink(temp_file)
    
    def test_failing_case(self):
        """Test a case where the control should fail."""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("id,value\\n")
            f.write("1,50\\n")
            f.write("2,150\\n")  # Exceeds threshold
            f.write("3,90\\n")
            temp_file = f.name
        
        try:
            control = {control_id}Control(data_file=temp_file)
            result = control.run()
            
            self.assertFalse(result.passed)
            self.assertEqual(result.control_id, "{control_id}")
        finally:
            os.unlink(temp_file)
''')
    
    example_dir = os.path.join(base_dir, 'examples')
    with open(os.path.join(example_dir, f'{control_id.lower()}_example.py'), 'w') as f:
        f.write(f'''"""
{control_id} Control Example

This script demonstrates how to use the {control_id}Control.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.{control_id}.control import {control_id}Control

data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', 'src', 'business_controls_framework',
                                         'controls', '{control_id}', 'data', 'sample.csv'))

if not os.path.exists(data_file):
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, 'w') as f:
        f.write("id,value\\n")
        f.write("1,50\\n")
        f.write("2,150\\n")  # Exceeds threshold
        f.write("3,90\\n")

control = {control_id}Control(data_file=data_file)
result = control.run()

print(f"Control ID: {{result.control_id}}")
print(f"Passed: {{result.passed}}")
print("Reasons:")
for reason in result.reasons:
    print(f"  - {{reason}}")

if not result.passed:
    print("\\nViolations:")
    for item in result.details.get("query_result", {{}}).get("results", []):
        value = item.get("value")
        if value is not None and float(value) > 100:
            print(f"  - ID {{item.get('id')}}: Value {{value}} exceeds threshold 100")
''')
    
    print(f"Created control {control_id} in {new_control_dir}")
    print(f"Created test file in {os.path.join(test_dir, f'test_{control_id}.py')}")
    print(f"Created example script in {os.path.join(example_dir, f'{control_id.lower()}_example.py')}")
    print("\nNext steps:")
    print(f"1. Update the main_v2.py file to register the new control")
    print(f"2. Customize the assertion logic in {os.path.join(new_control_dir, 'assertion.py')}")
    print(f"3. Run the tests: python -m unittest tests.test_controls.test_{control_id}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Create a new control directory with all required files")
    parser.add_argument("control_id", help="ID of the control (e.g., C789)")
    parser.add_argument("description", help="Description of the control")
    args = parser.parse_args()
    
    create_control_directory(args.control_id, args.description)


if __name__ == "__main__":
    main()
