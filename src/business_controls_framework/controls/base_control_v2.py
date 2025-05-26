"""
Base Control V2 class

This module defines the enhanced base class for all controls with custom assertions.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from ..assertion_engine.base_assertion import BaseAssertion
from ..query_engine.base_query import BaseQuery
from .base_control import ControlResult


class BaseControlV2:
    """Enhanced base class for all controls with custom assertions."""
    
    def __init__(self, control_id: str, description: str):
        """
        Initialize a control.
        
        Args:
            control_id: Unique identifier for the control
            description: Description of what the control checks
        """
        self.control_id = control_id
        self.description = description
        
    def create_query(self) -> BaseQuery:
        """
        Create a query for this control.
        
        Returns:
            Query to execute
        """
        raise NotImplementedError("Subclasses must implement create_query()")
        
    def create_assertion(self) -> BaseAssertion:
        """
        Create an assertion for this control.
        
        Returns:
            Assertion to evaluate
        """
        raise NotImplementedError("Subclasses must implement create_assertion()")
        
    def get_assertion_params(self) -> Dict[str, Any]:
        """
        Get parameters for the assertion.
        
        Returns:
            Parameters for the assertion
        """
        raise NotImplementedError("Subclasses must implement get_assertion_params()")
        
    def run(self) -> ControlResult:
        """
        Run the control test.
        
        Returns:
            ControlResult: The result of the control test
        """
        query = self.create_query()
        query_result = query.execute()
        
        assertion = self.create_assertion()
        passed, reasons = assertion.evaluate(query_result, self.get_assertion_params())
        
        return ControlResult(
            control_id=self.control_id,
            passed=passed,
            reasons=reasons,
            details={"query_result": query_result}
        )
