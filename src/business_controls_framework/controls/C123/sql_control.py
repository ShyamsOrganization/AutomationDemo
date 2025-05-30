"""
SQL-based Control C123

This module implements the C123 control for checking employee bonuses using SQLite.
"""
from typing import Dict, Any, List, Optional

from ...controls.base_control import BaseControl, ControlResult
from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from ...assertion_engine.assertion_evaluator import AssertionEvaluator


class C123SQLControl(BaseControl):
    """
    Control for checking employee bonuses using SQLite database.
    
    This control uses the max_percentage assertion to verify that employee
    bonuses do not exceed 20% of their salary. The control requires
    a SQLite database with 'salary' and 'bonus' fields.
    
    Input data: Employee data (SQLite database with salary and bonus columns)
    Assertion: max_percentage (from central registry)
    """
    
    def __init__(self, data_file: str, control_id: Optional[str] = None, description: Optional[str] = None):
        """
        Initialize the C123 SQL control.
        
        Args:
            data_file: Path to the employee SQLite database file
            control_id: Optional custom control ID (defaults to "C123_SQL")
            description: Optional custom description
        """
        super().__init__(
            control_id=control_id or "C123_SQL",
            description=description or "Check that employee bonuses are not more than 20% of salary (SQLite version)"
        )
        self.data_file = data_file
        
    def run(self) -> ControlResult:
        """
        Run the control test.
        
        Returns:
            ControlResult: The result of the control test
        """
        connector = EnhancedSQLConnector(self.data_file)
        
        query_result = {
            "results": connector.execute_query("SELECT * FROM employees")
        }
        
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
