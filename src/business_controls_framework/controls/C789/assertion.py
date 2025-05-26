"""
Range Assertion for C789

This module provides a range assertion implementation for the C789 control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class RangeAssertion(BaseAssertion):
    """Range assertion implementation for C789 control."""
    
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
                reasons.append(f"Missing field: {field}")
                passed = False
                continue
                
            try:
                value = float(value)
            except (ValueError, TypeError):
                reasons.append(f"Value '{value}' is not a number")
                passed = False
                continue
                
            if value < min_value or value > max_value:
                reasons.append(
                    f"Value {value} is outside the allowed range [{min_value}, {max_value}]"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values are within the allowed range [{min_value}, {max_value}]")
            
        return passed, reasons
