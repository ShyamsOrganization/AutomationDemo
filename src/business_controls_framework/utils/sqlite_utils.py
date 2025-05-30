"""
SQLite Utilities

This module provides utility functions for working with SQLite databases.
"""
import os
import csv
from typing import List, Dict, Any, Tuple, Optional

from ..data_connectors.enhanced_sql_connector import EnhancedSQLConnector


def csv_to_sqlite(csv_file: str, db_file: str, table_name: str) -> None:
    """
    Convert a CSV file to a SQLite database.
    
    Args:
        csv_file: Path to the CSV file
        db_file: Path to the SQLite database file
        table_name: Name of the table to create
    """
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        first_row = next(reader, None)
    
    columns = []
    for i, col_name in enumerate(header):
        if first_row and first_row[i].isdigit():
            col_type = "INTEGER"
        elif first_row and _is_float(first_row[i]):
            col_type = "REAL"
        else:
            col_type = "TEXT"
        columns.append((col_name, col_type))
    
    connector = EnhancedSQLConnector(db_file)
    connector.create_table(table_name, columns)
    
    with open(csv_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            processed_row = {}
            for key, value in row.items():
                if value.isdigit():
                    processed_row[key] = int(value)
                elif _is_float(value):
                    processed_row[key] = float(value)
                else:
                    processed_row[key] = value
            data.append(processed_row)
    
    connector.insert_data(table_name, data)
    connector.disconnect()


def setup_control_database(control_id: str, csv_file: str, table_name: Optional[str] = None) -> str:
    """
    Set up a SQLite database for a control from a CSV file.
    
    Args:
        control_id: ID of the control
        csv_file: Path to the CSV file
        table_name: Name of the table to create (defaults to 'data')
        
    Returns:
        Path to the created SQLite database file
    """
    control_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "controls", control_id)
    data_dir = os.path.join(control_dir, "data")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    db_file = os.path.join(data_dir, f"{control_id.lower()}.db")
    table_name = table_name or "data"
    
    csv_to_sqlite(csv_file, db_file, table_name)
    
    return db_file


def _is_float(value: str) -> bool:
    """Check if a string can be converted to a float."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
