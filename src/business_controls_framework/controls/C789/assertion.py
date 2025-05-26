"""
Custom Assertion for C789

This module provides a custom assertion implementation for the C789 control.
"""
from typing import Dict, Any, List, Tuple

from ...assertion_engine.base_assertion import BaseAssertion


class CustomAssertion(BaseAssertion):
    """Custom assertion implementation for C789 control."""
    
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
                reasons.append(f"Missing field: {field}")
                passed = False
                continue
                
            if value > threshold:
                reasons.append(
                    f"Value {value} exceeds threshold {threshold}"
                )
                passed = False
                
        if passed and not reasons:
            reasons.append(f"All values meet the criteria")
            
        return passed, reasons
