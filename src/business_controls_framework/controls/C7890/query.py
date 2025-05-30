"""
Query for C7890 control.

This module implements the query for retrieving employee bonus and salary data.
"""
from typing import Dict, Any, List

from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector


class BonusQuery:
    """
    Query for retrieving employee bonus and salary data from SQLite database.
    
    This query is used by the C7890 control to retrieve employee bonus and salary
    information for percentage checking.
    """
    
    def __init__(self, connector: EnhancedSQLConnector):
        """
        Initialize the bonus query.
        
        Args:
            connector: SQL connector for database access
        """
        self.connector = connector
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the query to retrieve employee bonus and salary data.
        
        Returns:
            Dictionary containing query results
        """
        results = self.connector.execute_query("SELECT * FROM employees")
        
        return {
            "results": results
        }
