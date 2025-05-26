"""
SQL Data Connector

This module provides a connector for SQL databases.
"""
from typing import List, Dict, Any, Optional
import sqlite3  # For demonstration; could use other DB libraries

from .base_connector import BaseConnector


class SQLConnector(BaseConnector):
    """Connector for SQL databases."""
    
    def __init__(self, connection_string: str):
        """
        Initialize a SQL connector.
        
        Args:
            connection_string: Connection string for the database
        """
        self.connection_string = connection_string
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self) -> None:
        """Establish connection to the database."""
        self.connection = sqlite3.connect(self.connection_string)
        
    def disconnect(self) -> None:
        """Close connection to the database."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query against the database.
        
        Args:
            query: SQL query to execute
            
        Returns:
            List of dictionaries representing the query results
        """
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        column_names = [description[0] for description in cursor.description]
        
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(column_names, row)))
            
        return results
