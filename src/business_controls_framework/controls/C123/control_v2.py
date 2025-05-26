"""
Control C123 V2

This module implements the C123 control for checking employee bonuses using the new architecture.
"""
from typing import Dict, Any, Optional

from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import MaxPercentageAssertion
from ...query_engine.base_query import BaseQuery
from ...assertion_engine.base_assertion import BaseAssertion


class C123ControlV2(BaseControlV2):
    """
    Control for checking employee bonuses using the new architecture.
    
    This control uses the MaxPercentageAssertion to verify that employee
    bonuses do not exceed 20% of their salary. The control requires
    employee data with 'salary' and 'bonus' fields.
    
    Input data: Employee data (CSV file with salary and bonus columns)
    Assertion: MaxPercentageAssertion
    """
    
    def __init__(self, data_file: str, control_id: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize the C123 control.
        
        Args:
            data_file: Path to the employee data file
            control_id: Optional custom control ID (defaults to "C123")
            description: Optional custom description
        """
        super().__init__(
            control_id=control_id or "C123",
            description=description or "Check that employee bonuses are not more than 20% of salary"
        )
        self.data_file = data_file
        
    def create_query(self) -> BaseQuery:
        """
        Create a query for this control.
        
        Returns:
            Query to execute
        """
        connector = CSVConnector(self.data_file)
        return SimpleQuery(connector)
        
    def create_assertion(self) -> BaseAssertion:
        """
        Create an assertion for this control.
        
        Returns:
            Assertion to evaluate
        """
        return MaxPercentageAssertion()
        
    def get_assertion_params(self) -> Dict[str, Any]:
        """
        Get parameters for the assertion.
        
        Returns:
            Parameters for the assertion
        """
        return {
            "value_field": "bonus",
            "base_field": "salary",
            "max_percentage": 20
        }
