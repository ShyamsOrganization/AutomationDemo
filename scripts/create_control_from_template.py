#!/usr/bin/env python3
"""
Control Creation Script from YAML Template

This script processes a YAML template file to generate a new control with all required files.
Non-technical users can define controls using the template and this script will handle the implementation.
"""
import os
import sys
import argparse
import yaml
import csv
from tempfile import NamedTemporaryFile


def create_control_from_template(template_file):
    """Create a new control from a YAML template file."""
    with open(template_file, 'r') as f:
        try:
            template = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML template: {e}")
            return False
    
    required_fields = ['control_id', 'description', 'assertion', 'data_file']
    for field in required_fields:
        if field not in template:
            print(f"Error: Missing required field '{field}' in template")
            return False
    
    control_id = template['control_id']
    description = template['description']
    assertion_config = template['assertion']
    data_file = template['data_file']
    
    assertion_type = assertion_config.get('type', 'custom')
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    controls_dir = os.path.join(base_dir, 'src', 'business_controls_framework', 'controls')
    new_control_dir = os.path.join(controls_dir, control_id)
    data_dir = os.path.join(new_control_dir, 'data')
    
    os.makedirs(new_control_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    
    if 'sample_data' in template:
        sample_data = template['sample_data'].strip()
        data_file_path = os.path.join(data_dir, data_file)
        
        with open(data_file_path, 'w') as f:
            lines = sample_data.split('\n')
            for line in lines:
                if not line.strip().startswith('#'):
                    f.write(line + '\n')
        print(f"Created sample data file: {data_file_path}")
    
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
    
    assertion_class_name = f"{''.join(word.capitalize() for word in assertion_type.split('_'))}Assertion"
    
    with open(os.path.join(new_control_dir, 'assertion.py'), 'w') as f:
        if assertion_type == 'range':
            f.write(create_range_assertion(control_id, assertion_class_name))
        elif assertion_type == 'max_percentage':
            f.write(create_max_percentage_assertion(control_id, assertion_class_name))
        elif assertion_type == 'threshold':
            f.write(create_threshold_assertion(control_id, assertion_class_name))
        else:
            f.write(create_custom_assertion(control_id, assertion_class_name))
    
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
    
    with open(os.path.join(new_control_dir, 'control.py'), 'w') as f:
        f.write(create_control_implementation(control_id, description, assertion_type, assertion_class_name, assertion_config))
    
    test_dir = os.path.join(base_dir, 'tests', 'test_controls')
    with open(os.path.join(test_dir, f'test_{control_id}.py'), 'w') as f:
        f.write(create_test_file(control_id, assertion_type, assertion_config))
    
    example_dir = os.path.join(base_dir, 'examples')
    with open(os.path.join(example_dir, f'{control_id.lower()}_example.py'), 'w') as f:
        f.write(create_example_script(control_id, description, data_file))
    
    print(f"Created control {control_id} in {new_control_dir}")
    print(f"Created test file in {os.path.join(test_dir, f'test_{control_id}.py')}")
    print(f"Created example script in {os.path.join(example_dir, f'{control_id.lower()}_example.py')}")
    print("\nNext steps:")
    print(f"1. Update the main_v2.py file to register the new control")
    print(f"2. Run the tests: python -m unittest tests.test_controls.test_{control_id}")
    
    return True


def create_range_assertion(control_id, assertion_class_name):
    """Create a range assertion implementation."""
    return f'''"""
Range Assertion for {control_id}

This module provides a range assertion implementation for the {control_id} control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class {assertion_class_name}(BaseAssertion):
    """Range assertion implementation for {control_id} control."""
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the assertion against data.
        
        Args:
            data: Data to evaluate
            params: Parameters for the assertion
                - field: Field to check
                - min_value: Minimum allowed value
                - max_value: Maximum allowed value
                
        Returns:
            Tuple of (passed, reasons)
        """
        field = params.get("field")
        min_value = params.get("min_value")
        max_value = params.get("max_value")
        
        if not all([field, min_value is not None, max_value is not None]):
            return False, ["Missing required parameters for range assertion"]
            
        results = data.get("results", [])
        passed = True
        reasons = []
        
        for item in results:
            value = item.get(field)
            
            if value is None:
                reasons.append(f"Missing field: {{field}}")
                passed = False
                continue
                
            try:
                value = float(value)
            except (ValueError, TypeError):
                reasons.append(f"Value '{{value}}' is not a number")
                passed = False
                continue
                
            if value < min_value or value > max_value:
                reasons.append(
                    f"Value {{value}} is outside the allowed range [{{min_value}}, {{max_value}}]"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values are within the allowed range [{{min_value}}, {{max_value}}]")
            
        return passed, reasons
'''


def create_max_percentage_assertion(control_id, assertion_class_name):
    """Create a max percentage assertion implementation."""
    return f'''"""
Max Percentage Assertion for {control_id}

This module provides a max percentage assertion implementation for the {control_id} control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class {assertion_class_name}(BaseAssertion):
    """Max percentage assertion implementation for {control_id} control."""
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the assertion against data.
        
        Args:
            data: Data to evaluate
            params: Parameters for the assertion
                - value_field: Field containing the value to check
                - base_field: Field containing the base value
                - max_percentage: Maximum allowed percentage
                
        Returns:
            Tuple of (passed, reasons)
        """
        value_field = params.get("value_field")
        base_field = params.get("base_field")
        max_percentage = params.get("max_percentage")
        
        if not all([value_field, base_field, max_percentage is not None]):
            return False, ["Missing required parameters for max percentage assertion"]
            
        results = data.get("results", [])
        passed = True
        reasons = []
        
        for item in results:
            value = item.get(value_field)
            base = item.get(base_field)
            
            if value is None or base is None:
                reasons.append(f"Missing fields: {{value_field}} or {{base_field}}")
                passed = False
                continue
                
            try:
                value = float(value)
                base = float(base)
            except (ValueError, TypeError):
                reasons.append(f"Values '{{value}}' or '{{base}}' are not numbers")
                passed = False
                continue
                
            if base == 0:
                reasons.append(f"Base value is zero, cannot calculate percentage")
                passed = False
                continue
                
            percentage = (value / base) * 100
            
            if percentage > max_percentage:
                reasons.append(
                    f"Value {{value}} is {{percentage:.2f}}% of {{base}}, which exceeds the maximum allowed {{max_percentage}}%"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values are within the maximum allowed percentage of {{max_percentage}}%")
            
        return passed, reasons
'''


def create_threshold_assertion(control_id, assertion_class_name):
    """Create a threshold assertion implementation."""
    return f'''"""
Threshold Assertion for {control_id}

This module provides a threshold assertion implementation for the {control_id} control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class {assertion_class_name}(BaseAssertion):
    """Threshold assertion implementation for {control_id} control."""
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the assertion against data.
        
        Args:
            data: Data to evaluate
            params: Parameters for the assertion
                - field: Field to check
                - threshold: Threshold value
                - operator: Comparison operator (>, <, >=, <=, ==, !=)
                
        Returns:
            Tuple of (passed, reasons)
        """
        field = params.get("field")
        threshold = params.get("threshold")
        operator = params.get("operator", ">")
        
        if not all([field, threshold is not None, operator]):
            return False, ["Missing required parameters for threshold assertion"]
            
        results = data.get("results", [])
        passed = True
        reasons = []
        
        for item in results:
            value = item.get(field)
            
            if value is None:
                reasons.append(f"Missing field: {{field}}")
                passed = False
                continue
                
            try:
                value = float(value)
                threshold = float(threshold)
            except (ValueError, TypeError):
                reasons.append(f"Value '{{value}}' is not a number")
                passed = False
                continue
                
            comparison_failed = False
            
            if operator == ">":
                comparison_failed = not (value > threshold)
            elif operator == "<":
                comparison_failed = not (value < threshold)
            elif operator == ">=":
                comparison_failed = not (value >= threshold)
            elif operator == "<=":
                comparison_failed = not (value <= threshold)
            elif operator == "==":
                comparison_failed = not (value == threshold)
            elif operator == "!=":
                comparison_failed = not (value != threshold)
            else:
                reasons.append(f"Invalid operator: {{operator}}")
                passed = False
                continue
                
            if comparison_failed:
                reasons.append(
                    f"Value {{value}} does not satisfy {{operator}} {{threshold}}"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values satisfy {{operator}} {{threshold}}")
            
        return passed, reasons
'''


def create_custom_assertion(control_id, assertion_class_name):
    """Create a custom assertion implementation."""
    return f'''"""
Custom Assertion for {control_id}

This module provides a custom assertion implementation for the {control_id} control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class {assertion_class_name}(BaseAssertion):
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
                
            try:
                value = float(value)
            except (ValueError, TypeError):
                reasons.append(f"Value '{{value}}' is not a number")
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
'''


def create_control_implementation(control_id, description, assertion_type, assertion_class_name, assertion_config):
    """Create a control implementation."""
    if assertion_type == 'range':
        params_code = f'''{{
            "field": "{assertion_config.get('field', 'value')}",
            "min_value": {assertion_config.get('min_value', 0)},
            "max_value": {assertion_config.get('max_value', 100)}
        }}'''
    elif assertion_type == 'max_percentage':
        params_code = f'''{{
            "value_field": "{assertion_config.get('value_field', 'value')}",
            "base_field": "{assertion_config.get('base_field', 'base')}",
            "max_percentage": {assertion_config.get('max_percentage', 20)}
        }}'''
    elif assertion_type == 'threshold':
        params_code = f'''{{
            "field": "{assertion_config.get('field', 'value')}",
            "threshold": {assertion_config.get('threshold', 100)},
            "operator": "{assertion_config.get('operator', '>')}"
        }}'''
    else:
        params_code = f'''{{
            "field": "{assertion_config.get('field', 'value')}",
            "threshold": {assertion_config.get('threshold', 100)}
        }}'''
    
    return f'''"""
{control_id} Control Implementation

{description}
"""
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import {assertion_class_name}


class {control_id}Control(BaseControlV2):
    """
    {description}
    
    This control uses the {assertion_class_name} to verify data meets specific criteria.
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
        return {assertion_class_name}()
    
    def get_assertion_params(self):
        """
        Get parameters for the assertion.
        
        Returns:
            Dictionary of parameters
        """
        return {params_code}
'''


def create_test_file(control_id, assertion_type, assertion_config):
    """Create a test file for the control."""
    if assertion_type == 'range':
        field = assertion_config.get('field', 'value')
        min_value = assertion_config.get('min_value', 0)
        max_value = assertion_config.get('max_value', 100)
        
        passing_data = f'''id,{field}\\n1,{min_value + 1}\\n2,{max_value - 1}\\n'''
        failing_data = f'''id,{field}\\n1,{min_value - 1}\\n2,{max_value + 1}\\n'''
    elif assertion_type == 'max_percentage':
        value_field = assertion_config.get('value_field', 'value')
        base_field = assertion_config.get('base_field', 'base')
        max_percentage = assertion_config.get('max_percentage', 20)
        
        passing_data = f'''id,{value_field},{base_field}\\n1,{max_percentage - 5},100\\n2,{max_percentage - 1},100\\n'''
        failing_data = f'''id,{value_field},{base_field}\\n1,{max_percentage + 5},100\\n2,{max_percentage + 10},100\\n'''
    elif assertion_type == 'threshold':
        field = assertion_config.get('field', 'value')
        threshold = assertion_config.get('threshold', 100)
        operator = assertion_config.get('operator', '>')
        
        if operator in ['>', '>=']:
            passing_data = f'''id,{field}\\n1,{threshold + 10}\\n2,{threshold + 20}\\n'''
            failing_data = f'''id,{field}\\n1,{threshold - 10}\\n2,{threshold - 20}\\n'''
        else:
            passing_data = f'''id,{field}\\n1,{threshold - 10}\\n2,{threshold - 20}\\n'''
            failing_data = f'''id,{field}\\n1,{threshold + 10}\\n2,{threshold + 20}\\n'''
    else:
        field = assertion_config.get('field', 'value')
        threshold = assertion_config.get('threshold', 100)
        
        passing_data = f'''id,{field}\\n1,{threshold - 10}\\n2,{threshold - 20}\\n'''
        failing_data = f'''id,{field}\\n1,{threshold + 10}\\n2,{threshold + 20}\\n'''
    
    return f'''"""
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
            f.write("{passing_data}")
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
            f.write("{failing_data}")
            temp_file = f.name
        
        try:
            control = {control_id}Control(data_file=temp_file)
            result = control.run()
            
            self.assertFalse(result.passed)
            self.assertEqual(result.control_id, "{control_id}")
        finally:
            os.unlink(temp_file)
'''


def create_example_script(control_id, description, data_file):
    """Create an example script for the control."""
    return f'''"""
{control_id} Control Example

This script demonstrates how to use the {control_id}Control.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.{control_id}.control import {control_id}Control

data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', 'src', 'business_controls_framework',
                                         'controls', '{control_id}', 'data', '{data_file}'))

control = {control_id}Control(data_file=data_file)
result = control.run()

print(f"Control ID: {{result.control_id}}")
print(f"Description: {description}")
print(f"Passed: {{result.passed}}")
print("Reasons:")
for reason in result.reasons:
    print(f"  - {{reason}}")

if not result.passed:
    print("\\nViolations:")
    for item in result.details.get("query_result", {{}}).get("results", []):
        print(f"  - ID {{item.get('id')}}: {{item}}")
'''


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Create a new control from a YAML template file")
    parser.add_argument("template_file", help="Path to the YAML template file")
    args = parser.parse_args()
    
    if not os.path.exists(args.template_file):
        print(f"Error: Template file '{args.template_file}' does not exist")
        return 1
    
    success = create_control_from_template(args.template_file)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
