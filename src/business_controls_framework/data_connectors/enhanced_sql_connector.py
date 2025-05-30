"""
Enhanced SQL Data Connector

This module provides an enhanced connector for SQL databases with additional
functionality for creating tables and inserting data.
"""
from typing import List, Dict, Any, Optional, Tuple
import sqlite3
import os

from .sql_connector import SQLConnector


class EnhancedSQLConnector(SQLConnector):
    """
    Enhanced connector for SQL databases with additional functionality.
    
    This connector extends the base SQLConnector with methods for:
    - Creating tables
    - Inserting data
    - Executing transactions
    - Managing schema
    """
    
    def __init__(self, connection_string: str, create_if_not_exists: bool = True):
        """
        Initialize an enhanced SQL connector.
        
        Args:
            connection_string: Connection string for the database
            create_if_not_exists: Whether to create the database file if it doesn't exist
        """
        super().__init__(connection_string)
        self.create_if_not_exists = create_if_not_exists
        
        if create_if_not_exists:
            db_dir = os.path.dirname(connection_string)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
    
    def create_table(self, table_name: str, columns: List[Tuple[str, str]], if_not_exists: bool = True) -> None:
        """
        Create a table in the database.
        
        Args:
            table_name: Name of the table to create
            columns: List of (column_name, column_type) tuples
            if_not_exists: Whether to add IF NOT EXISTS to the SQL statement
        """
        if not self.connection:
            self.connect()
            
        column_defs = [f"{name} {type_}" for name, type_ in columns]
        exists_clause = "IF NOT EXISTS " if if_not_exists else ""
        
        query = f"CREATE TABLE {exists_clause}{table_name} ({', '.join(column_defs)})"
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
    
    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        """
        Insert data into a table.
        
        Args:
            table_name: Name of the table to insert into
            data: List of dictionaries with column names as keys
        """
        if not data:
            return
            
        if not self.connection:
            self.connect()
            
        columns = list(data[0].keys())
        
        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        values = []
        for item in data:
            row = [item.get(column) for column in columns]
            values.append(row)
        
        cursor = self.connection.cursor()
        cursor.executemany(query, values)
        self.connection.commit()
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check
            
        Returns:
            True if the table exists, False otherwise
        """
        if not self.connection:
            self.connect()
            
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        return cursor.fetchone() is not None
    
    def execute_transaction(self, queries: List[str]) -> None:
        """
        Execute multiple queries in a single transaction.
        
        Args:
            queries: List of SQL queries to execute
        """
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        try:
            for query in queries:
                cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
