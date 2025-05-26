"""
Max Percentage Assertion

This module provides an assertion for checking that one value is not more than a percentage of another value.
"""
from typing import Dict, Any, List, Tuple

from .base_assertion import BaseAssertion


class MaxPercentageAssertion(BaseAssertion):
    """Assertion for checking that one value is not more than a percentage of another value."""
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the assertion against data.
        
        Args:
            data: Data to evaluate
            params: Parameters for the assertion, including:
                - value_field: Field containing the value to check
                - base_field: Field containing the base value
                - max_percentage: Maximum allowed percentage
                
        Returns:
            Tuple of (passed, reasons)
        """
        value_field = params.get("value_field")
        base_field = params.get("base_field")
        max_percentage = params.get("max_percentage")
        
        if not all([value_field, base_field, max_percentage]):
            return False, ["Missing required parameters for max_percentage assertion"]
            
        results = data.get("results", [])
        passed = True
        reasons = []
        
        for item in results:
            value = item.get(value_field)
            base = item.get(base_field)
            
            if value is None or base is None:
                reasons.append(f"Missing fields: {value_field}={value}, {base_field}={base}")
                passed = False
                continue
                
            if base == 0:
                reasons.append(f"Base value ({base_field}) is zero, cannot calculate percentage")
                passed = False
                continue
                
            percentage = (value / base) * 100
            
            if percentage > max_percentage:
                reasons.append(
                    f"Value {value} is {percentage:.2f}% of {base}, "
                    f"which exceeds the maximum allowed {max_percentage}%"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values are within the maximum {max_percentage}% limit")
            
        return passed, reasons
