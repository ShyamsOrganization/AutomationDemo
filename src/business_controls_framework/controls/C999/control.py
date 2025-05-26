"""
C999 Control Implementation

Check customer account balances
"""
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import RangeAssertion


class C999Control(BaseControlV2):
    """
    Check customer account balances
    
    This control uses the RangeAssertion to verify data meets specific criteria.
    """
    
    def __init__(self, data_file, control_id="C999", description="Check customer account balances"):
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
