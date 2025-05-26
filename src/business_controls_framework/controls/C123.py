"""
Control C123

This module implements the C123 control for checking employee bonuses.
"""
from typing import Dict, Any, List, Optional

from ..controls.base_control import BaseControl, ControlResult
from ..data_connectors.csv_connector import CSVConnector
from ..query_engine.query_builder import QueryBuilder
from ..assertion_engine.assertion_evaluator import AssertionEvaluator


class C123Control(BaseControl):
    """Control for checking employee bonuses."""
    
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
        
    def run(self) -> ControlResult:
        """
        Run the control test.
        
        Returns:
            ControlResult: The result of the control test
        """
        connector = CSVConnector(self.data_file)
        query_builder = QueryBuilder(connector)
        
        query_result = query_builder.execute("all")
        
        evaluator = AssertionEvaluator()
        
        passed, reasons = evaluator.evaluate(
            query_result,
            "max_percentage",
            {
                "value_field": "bonus",
                "base_field": "salary",
                "max_percentage": 20
            }
        )
        
        return ControlResult(
            control_id=self.control_id,
            passed=passed,
            reasons=reasons,
            details={"query_result": query_result}
        )
