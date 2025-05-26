"""
Control C456

This module implements the C456 control for checking interest rates using the new architecture.
"""
from typing import Dict, Any, Optional

from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import RangeAssertion
from ...query_engine.base_query import BaseQuery
from ...assertion_engine.base_assertion import BaseAssertion


class C456Control(BaseControlV2):
    """
    Control for checking interest rates.
    
    This control uses the RangeAssertion to verify that loan interest rates
    are within the acceptable range of 2% to 15%. The control requires
    loan data with an 'interest_rate' field.
    
    Input data: Loan data (CSV file with interest_rate column)
    Assertion: RangeAssertion
    """
    
    def __init__(self, data_file: str, control_id: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize the C456 control.
        
        Args:
            data_file: Path to the loan data file
            control_id: Optional custom control ID (defaults to "C456")
            description: Optional custom description
        """
        super().__init__(
            control_id=control_id or "C456",
            description=description or "Check that interest rates are within the allowed range (2% to 15%)"
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
        return RangeAssertion()
        
    def get_assertion_params(self) -> Dict[str, Any]:
        """
        Get parameters for the assertion.
        
        Returns:
            Parameters for the assertion
        """
        return {
            "field": "interest_rate",
            "min_value": 2.0,
            "max_value": 15.0
        }
