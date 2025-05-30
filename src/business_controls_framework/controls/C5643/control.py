"""
C5643 Control for checking employee salaries.

This control checks that no employee has a salary exceeding 100k USD.
"""
from typing import Dict, Any, List, Optional

from ...controls.base_control_v2 import BaseControlV2, ControlResult
from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from .assertion import ThresholdAssertion
from .query import SalaryQuery


class C5643Control(BaseControlV2):
    """
    Control for checking employee salaries using SQLite database.
    
    This control uses the threshold assertion to verify that no employee
    has a salary exceeding 100k USD. The control requires a SQLite database
    with a 'salary' field.
    
    Input data: Employee data (SQLite database with salary column)
    Assertion: ThresholdAssertion (custom implementation)
    """
    
    def __init__(self, data_file: str, control_id: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize the C5643 control.
        
        Args:
            data_file: Path to the employee SQLite database file
            control_id: Optional custom control ID (defaults to "C5643")
            description: Optional custom description
        """
        super().__init__(
            control_id=control_id or "C5643",
            description=description or "Check that no employee has a salary exceeding 100k USD"
        )
        self.data_file = data_file
    
    def create_query(self):
        """
        Create the query for this control.
        
        Returns:
            SalaryQuery instance
        """
        connector = EnhancedSQLConnector(self.data_file)
        return SalaryQuery(connector)
    
    def create_assertion(self):
        """
        Create the assertion for this control.
        
        Returns:
            ThresholdAssertion instance
        """
        return ThresholdAssertion()
    
    def get_assertion_params(self):
        """
        Get the parameters for the assertion.
        
        Returns:
            Dictionary with assertion parameters
        """
        return {
            "field": "salary",
            "threshold": 100000
        }
