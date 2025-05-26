"""
C789 Control Implementation

Check customer credit limits
"""
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import CustomAssertion


class C789Control(BaseControlV2):
    """
    Check customer credit limits
    
    This control uses the CustomAssertion to verify data meets specific criteria.
    """
    
    def __init__(self, data_file, control_id="C789", description="Check customer credit limits"):
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
        return CustomAssertion()
    
    def get_assertion_params(self):
        """
        Get parameters for the assertion.
        
        Returns:
            Dictionary of parameters
        """
        return {
            "field": "value",
            "threshold": 100
        }
