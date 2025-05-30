"""
Assertion for C7890 control.

This module implements the high bonus assertion for checking employee bonuses.
"""
from typing import Dict, Any, List, Tuple


class HighBonusAssertion:
    """
    Assertion that checks if bonus values exceed a specified percentage of salary.
    
    This assertion is used by the C7890 control to verify that employee
    bonuses do not exceed a specified percentage (30%) of their salary.
    """
    
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate the high bonus assertion on the provided data.
        
        Args:
            data: Dictionary containing query results
            params: Parameters for the assertion including:
                - value_field: The field containing the value to check (bonus)
                - base_field: The field containing the base value (salary)
                - max_percentage: The maximum allowed percentage
                
        Returns:
            Tuple containing:
                - Boolean indicating if the assertion passed
                - List of reasons for failure
        """
        value_field = params.get("value_field")
        base_field = params.get("base_field")
        max_percentage = params.get("max_percentage")
        
        if not value_field or not base_field or max_percentage is None:
            return False, ["Missing required parameters: value_field, base_field, and max_percentage"]
        
        results = data.get("results", [])
        reasons = []
        
        for item in results:
            value = item.get(value_field)
            base = item.get(base_field)
            
            if value is not None and base is not None and base > 0:
                percentage = (value / base) * 100
                if percentage > max_percentage:
                    reasons.append(
                        f"Value {value} is {percentage:.2f}% of {base}, which exceeds the maximum allowed {max_percentage}%"
                    )
        
        return len(reasons) == 0, reasons
