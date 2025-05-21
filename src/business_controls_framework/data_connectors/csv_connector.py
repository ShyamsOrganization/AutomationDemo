"""
CSV Data Connector

This module provides a connector for CSV files.
"""
import csv
from typing import List, Dict, Any, Optional

from .base_connector import BaseConnector


class CSVConnector(BaseConnector):
    """Connector for CSV files."""
    
    def __init__(self, file_path: str):
        """
        Initialize a CSV connector.
        
        Args:
            file_path: Path to the CSV file
        """
        self.file_path = file_path
        self.data: Optional[List[Dict[str, Any]]] = None
        
    def connect(self) -> None:
        """Load data from the CSV file."""
        self.data = []
        with open(self.file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                processed_row = {}
                for key, value in row.items():
                    try:
                        if value.isdigit():
                            processed_row[key] = int(value)
                        else:
                            try:
                                processed_row[key] = float(value)
                            except ValueError:
                                processed_row[key] = value
                    except (ValueError, AttributeError):
                        processed_row[key] = value
                self.data.append(processed_row)
    
    def disconnect(self) -> None:
        """Clear loaded data."""
        self.data = None
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a query against the CSV data.
        
        For CSV, the query is a simple filter expression.
        Currently supports basic queries like "all" to return all data.
        
        Args:
            query: Query string to execute
            
        Returns:
            List of dictionaries representing the query results
        """
        if self.data is None:
            self.connect()
            
        if query.lower() == "all":
            return self.data or []
            
        return self.data or []
