"""
Base Data Connector

This module defines the base class for all data connectors.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseConnector(ABC):
    """Base class for all data connectors."""
    
    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the data source."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a query against the data source.
        
        Args:
            query: Query string to execute
            
        Returns:
            List of dictionaries representing the query results
        """
        pass
