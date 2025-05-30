"""
Assertion for C5643 control.

This module implements the threshold assertion for checking employee salaries.
"""
from typing import Dict, Any, List, Tuple


class ThresholdAssertion:
    """
    Assertion that checks if values are below a specified threshold.
    
    This assertion is used by the C5643 control to verify that employee
    salaries do not exceed a specified threshold (100k USD).
    """
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the threshold assertion on the provided data.
        
        Args:
            data: Dictionary containing query results
            params: Parameters for the assertion including:
                - field: The field to check
                - threshold: The maximum allowed value
                
        Returns:
            Tuple containing:
                - Boolean indicating if the assertion passed
                - List of reasons for failure
        """
        field = params.get("field")
        threshold = params.get("threshold")
        
        if not field or threshold is None:
            return False, ["Missing required parameters: field and threshold"]
        
        results = data.get("results", [])
        reasons = []
        
        for item in results:
            value = item.get(field)
            
            if value is not None and value > threshold:
                reasons.append(f"Value {value} exceeds the maximum allowed threshold of {threshold}")
        
        return len(reasons) == 0, reasons
