"""
C999 Control Implementation

Check customer account balances are within acceptable limits
"""
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from .query import SQLQuery
from .assertion import RangeAssertion


class C999Control(BaseControlV2):
    """
    Check customer account balances are within acceptable limits
    
    This control uses SQLite database and the RangeAssertion to verify
    that account balances are within acceptable limits.
    """
    
    def __init__(self, data_file, control_id="C999", description="Check customer account balances are within acceptable limits"):
        """
        Initialize the control.
        
        Args:
            data_file: Path to the SQLite database file
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
        connector = EnhancedSQLConnector(self.data_file)
        return SQLQuery(connector)
    
    def create_assertion(self):
        """
        Create an assertion for this control.
        
        Returns:
            Assertion object
        """
        return RangeAssertion()
    
    def get_assertion_params(self):
        """
        Get parameters for the assertion.
        
        Returns:
            Dictionary of parameters
        """
        return {
            "field": "account_balance",
            "min_value": 0,
            "max_value": 1000000
        }
