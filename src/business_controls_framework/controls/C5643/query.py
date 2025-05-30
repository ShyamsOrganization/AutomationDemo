"""
Query for C5643 control.

This module implements the query for retrieving employee salary data.
"""
from typing import Dict, Any, List

from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector


class SalaryQuery:
    """
    Query for retrieving employee salary data from SQLite database.
    
    This query is used by the C5643 control to retrieve employee salary
    information for threshold checking.
    """
    
    def __init__(self, connector: EnhancedSQLConnector):
        """
        Initialize the salary query.
        
        Args:
            connector: SQL connector for database access
        """
        self.connector = connector
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the query to retrieve employee salary data.
        
        Returns:
            Dictionary containing query results
        """
        results = self.connector.execute_query("SELECT * FROM employees")
        
        return {
            "results": results
        }
