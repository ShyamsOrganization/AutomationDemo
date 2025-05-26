"""
Base Control class

This module defines the base class for all controls.
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class ControlResult:
    """Result of a control test."""
    control_id: str
    passed: bool
    reasons: List[str]
    details: Optional[Dict[str, Any]] = None


class BaseControl:
    """Base class for all controls."""
    
    def __init__(self, control_id: str, description: str):
        """
        Initialize a control.
        
        Args:
            control_id: Unique identifier for the control
            description: Description of what the control checks
        """
        self.control_id = control_id
        self.description = description
        
    def run(self) -> ControlResult:
        """
        Run the control test.
        
        Returns:
            ControlResult: The result of the control test
        """
        raise NotImplementedError("Subclasses must implement run()")
