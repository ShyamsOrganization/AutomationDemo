"""
Setup SQLite Database for C999 Control

This script creates a SQLite database for the C999 control with sample data.
"""
import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')))

from src.business_controls_framework.data_connectors.enhanced_sql_connector import EnhancedSQLConnector


def setup_database():
    """Create a SQLite database for the C999 control."""
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.db")
    
    connector = EnhancedSQLConnector(db_file)
    
    connector.create_table(
        "accounts",
        [
            ("account_id", "TEXT"),
            ("customer_name", "TEXT"),
            ("account_balance", "REAL")
        ]
    )
    
    connector.insert_data(
        "accounts",
        [
            {"account_id": "A001", "customer_name": "John Smith", "account_balance": 5000},
            {"account_id": "A002", "customer_name": "Jane Doe", "account_balance": 750000},
            {"account_id": "A003", "customer_name": "Bob Johnson", "account_balance": 1200000},  # Exceeds max
            {"account_id": "A004", "customer_name": "Alice Williams", "account_balance": -500}   # Below min
        ]
    )
    
    connector.disconnect()
    print(f"Database created at {db_file}")
    return db_file


if __name__ == "__main__":
    setup_database()
