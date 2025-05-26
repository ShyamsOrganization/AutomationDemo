"""
Simple Query for C999

This module provides a simple query implementation for the C999 control.
"""
from typing import Dict, Any

from ...query_engine.base_query import BaseQuery


class SimpleQuery(BaseQuery):
    """Simple query implementation for C999 control."""
    
    def __init__(self, connector, query_string="all"):
        """
        Initialize a simple query.
        
        Args:
            connector: Data connector to use for executing queries
            query_string: Query string to execute
        """
        super().__init__(connector)
        self.query_string = query_string
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the query.
        
        Returns:
            Query results
        """
        results = self.connector.execute_query(self.query_string)
        return {"results": results}
