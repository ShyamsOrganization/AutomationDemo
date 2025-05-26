"""
Script to generate a large test file with employee data.
"""
import csv
import random
import os
from pathlib import Path

NUM_RECORDS = 1000
OUTPUT_FILE = Path("../tests/data/employees_large.csv")
FIRST_NAMES = ["John", "Jane", "Bob", "Alice", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", 
               "Ivy", "Jack", "Kate", "Leo", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Ryan", 
               "Sophia", "Thomas", "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zach"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
              "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White",
              "Lopez", "Lee", "Gonzalez", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Perez", "Hall"]
LOCATIONS = ["New York", "San Francisco", "Chicago", "Boston", "Seattle", "Los Angeles", "Austin", "Denver", 
             "Miami", "Atlanta", "Dallas", "Phoenix", "Philadelphia", "Houston", "Detroit", "Portland", 
             "Nashville", "San Diego", "Minneapolis", "Charlotte", "Indianapolis", "Washington DC", "Baltimore", 
             "Pittsburgh", "Cleveland", "Cincinnati", "St. Louis", "Kansas City", "Orlando", "Tampa"]

def generate_employee_data():
    """Generate random employee data."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    
    salary = random.randint(50000, 200000)
    
    age = random.randint(22, 65)
    
    location = random.choice(LOCATIONS)
    
    if random.random() < 0.85:  # 85% chance of being within limit
        bonus = int(salary * random.uniform(0.05, 0.19))
    else:  # 15% chance of exceeding limit
        bonus = int(salary * random.uniform(0.21, 0.30))
    
    return [name, salary, age, location, bonus]

def main():
    """Generate test data and write to CSV file."""
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(['name', 'salary', 'age', 'location', 'bonus'])
        
        for _ in range(NUM_RECORDS):
            writer.writerow(generate_employee_data())
    
    print(f"Generated {NUM_RECORDS} employee records in {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
