"""
C7890 Control for checking employee bonuses.

This control checks that no employee has a bonus exceeding 30% of their salary.
"""
from typing import Dict, Any, List, Optional

from ...controls.base_control_v2 import BaseControlV2, ControlResult
from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from .assertion import HighBonusAssertion
from .query import BonusQuery


class C7890Control(BaseControlV2):
    """
    Control for checking employee bonuses using SQLite database.
    
    This control uses the high bonus assertion to verify that no employee
    has a bonus exceeding 30% of their salary. The control requires a SQLite database
    with 'bonus' and 'salary' fields.
    
    Input data: Employee data (SQLite database with bonus and salary columns)
    Assertion: HighBonusAssertion (custom implementation)
    """
    
    def __init__(self, data_file: str, control_id: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize the C7890 control.
        
        Args:
            data_file: Path to the employee SQLite database file
            control_id: Optional custom control ID (defaults to "C7890")
            description: Optional custom description
        """
        super().__init__(
            control_id=control_id or "C7890",
            description=description or "Check that no employee has a bonus exceeding 30% of salary"
        )
        self.data_file = data_file
    
    def create_query(self):
        """
        Create the query for this control.
        
        Returns:
            BonusQuery instance
        """
        connector = EnhancedSQLConnector(self.data_file)
        return BonusQuery(connector)
    
    def create_assertion(self):
        """
        Create the assertion for this control.
        
        Returns:
            HighBonusAssertion instance
        """
        return HighBonusAssertion()
    
    def get_assertion_params(self):
        """
        Get the parameters for the assertion.
        
        Returns:
            Dictionary with assertion parameters
        """
        return {
            "value_field": "bonus",
            "base_field": "salary",
            "max_percentage": 30
        }
