"""
Example script demonstrating the use of SQLite with controls.

This script:
1. Creates a SQLite database from a CSV file
2. Sets up a control that uses the SQLite database
3. Runs the control to check account balances
"""
import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C999.control import C999Control
from src.business_controls_framework.data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from src.business_controls_framework.utils.sqlite_utils import setup_control_database


def create_sample_database():
    """Create a sample SQLite database for the C999 control."""
    control_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src", "business_controls_framework", "controls", "C999", "data"
    )
    
    if not os.path.exists(control_dir):
        os.makedirs(control_dir)
    
    db_file = os.path.join(control_dir, "accounts.db")
    
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
    return db_file


def main():
    """Run the example."""
    db_file = create_sample_database()
    
    control = C999Control(db_file)
    result = control.run()
    
    print(f"Control ID: {control.control_id}")
    print(f"Description: {control.description}")
    print(f"Passed: {result.passed}")
    print("Reasons:")
    for reason in result.reasons:
        print(f"  - {reason}")
    
    print("\nViolations:")
    for item in result.details.get("results", []):
        print(f"  - Account {item['account_id']}: {item['customer_name']} has balance ${item['account_balance']}")


if __name__ == "__main__":
    main()
