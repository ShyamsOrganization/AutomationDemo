"""
Base Query

This module defines the base interface for all queries.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from ..data_connectors.base_connector import BaseConnector


class BaseQuery(ABC):
    """Base interface for all queries."""
    
    def __init__(self, connector: BaseConnector):
        """
        Initialize a query.
        
        Args:
            connector: Data connector to use for executing queries
        """
        self.connector = connector
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Execute the query.
        
        Returns:
            Query results
        """
        pass
