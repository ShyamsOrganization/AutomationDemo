"""
Import Employees CSV to SQLite and Add More Records

This script:
1. Imports the employees.csv file to a SQLite database
2. Adds 1000 more employee records with similar structure
3. Verifies the total record count
"""
import os
import sys
import random
import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from src.business_controls_framework.utils.sqlite_utils import csv_to_sqlite


CSV_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "business_controls_framework", "controls", "C123", "data", "employees.csv"
)
DB_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "business_controls_framework", "controls", "C123", "data", "employees.db"
)
TABLE_NAME = "employees"
NUM_RECORDS_TO_ADD = 1000


def import_csv_to_sqlite():
    """Import the CSV file to SQLite."""
    print(f"Importing {CSV_FILE} to SQLite database {DB_FILE}...")
    csv_to_sqlite(CSV_FILE, DB_FILE, TABLE_NAME)
    print("Import complete.")


def generate_random_employee():
    """Generate a random employee record."""
    first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Lisa", 
                  "William", "Jennifer", "James", "Mary", "Christopher", "Elizabeth", 
                  "Daniel", "Jessica", "Matthew", "Susan", "Andrew", "Karen"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", 
                 "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", 
                 "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
    
    locations = ["New York", "San Francisco", "Chicago", "Boston", "Seattle", "Los Angeles", 
                "Austin", "Denver", "Miami", "Atlanta", "Dallas", "Phoenix", "Portland", 
                "Philadelphia", "Washington DC", "Houston", "San Diego", "Nashville", 
                "Minneapolis", "Detroit"]
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    salary = random.randint(50000, 200000)
    age = random.randint(22, 65)
    location = random.choice(locations)
    
    if random.random() < 0.1:  # 10% chance of high bonus
        bonus = int(salary * random.uniform(0.2, 0.3))
    else:
        bonus = int(salary * random.uniform(0.1, 0.2))
    
    return {
        "name": name,
        "salary": salary,
        "age": age,
        "location": location,
        "bonus": bonus
    }


def add_more_records():
    """Add more employee records to the SQLite database."""
    print(f"Adding {NUM_RECORDS_TO_ADD} more employee records...")
    
    connector = EnhancedSQLConnector(DB_FILE)
    
    employees = []
    for _ in range(NUM_RECORDS_TO_ADD):
        employees.append(generate_random_employee())
    
    connector.insert_data(TABLE_NAME, employees)
    connector.disconnect()
    
    print("Additional records added successfully.")


def verify_record_count():
    """Verify the total record count in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Total records in database: {count}")
    return count


def main():
    """Main function."""
    start_time = datetime.now()
    print(f"Starting import and data generation at {start_time}")
    
    import_csv_to_sqlite()
    
    add_more_records()
    
    total_records = verify_record_count()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"Process completed in {duration.total_seconds():.2f} seconds")
    print(f"Original CSV records + {NUM_RECORDS_TO_ADD} new records = {total_records} total records")


if __name__ == "__main__":
    main()
