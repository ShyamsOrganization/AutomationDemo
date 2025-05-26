"""
Base Assertion

This module defines the base interface for all assertions.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple


class BaseAssertion(ABC):
    """Base interface for all assertions."""
    
    @abstractmethod
    def evaluate(self, data: Dict[str, Any], params: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Evaluate an assertion against data.
        
        Args:
            data: Data to evaluate
            params: Parameters for the assertion
            
        Returns:
            Tuple of (passed, reasons)
        """
        pass
