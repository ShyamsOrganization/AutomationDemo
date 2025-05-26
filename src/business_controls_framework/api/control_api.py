"""
Control API

This module provides API endpoints for running control tests and retrieving results.
"""
from typing import Dict, Any, List, Optional

from ..controls.base_control import ControlResult


class ControlAPI:
    """API for running control tests and retrieving results."""
    
    def __init__(self):
        """Initialize the control API."""
        self.controls: Dict[str, Any] = {}
        self.results: Dict[str, ControlResult] = {}
        
    def register_control(self, control: Any) -> None:
        """
        Register a control with the API.
        
        Args:
            control: Control to register
        """
        self.controls[control.control_id] = control
        
    def run_control(self, control_id: str) -> ControlResult:
        """
        Run a control test.
        
        Args:
            control_id: ID of the control to run
            
        Returns:
            Result of the control test
        """
        if control_id not in self.controls:
            return ControlResult(
                control_id=control_id,
                passed=False,
                reasons=[f"Control {control_id} not found"],
                details=None
            )
            
        result = self.controls[control_id].run()
        self.results[control_id] = result
        return result
        
    def run_all_controls(self) -> List[ControlResult]:
        """
        Run all registered control tests.
        
        Returns:
            List of control test results
        """
        results = []
        for control_id in self.controls:
            results.append(self.run_control(control_id))
        return results
        
    def get_result(self, control_id: str) -> Optional[ControlResult]:
        """
        Get the result of a control test.
        
        Args:
            control_id: ID of the control
            
        Returns:
            Result of the control test, or None if not found
        """
        return self.results.get(control_id)
        
    def get_all_results(self) -> Dict[str, ControlResult]:
        """
        Get all control test results.
        
        Returns:
            Dictionary of control test results
        """
        return self.results
