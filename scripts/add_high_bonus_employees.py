"""
Script to add employees with high bonuses to the SQLite database.

This script adds test employees with bonuses exceeding 30% of their salary
to verify the C7890 control correctly identifies violations.
"""
import os
import sys
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def main():
    """Add employees with high bonuses to the database."""
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src", "business_controls_framework", "controls", "C123", "data", "employees.db"
    )
    
    high_bonus_employees = [
        ("John HighBonus", 100000, 35, "New York", 35000),  # 35% bonus
        ("Sarah Excessive", 80000, 42, "Chicago", 32000),    # 40% bonus
        ("Mike TooMuch", 120000, 38, "San Francisco", 48000) # 40% bonus
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for employee in high_bonus_employees:
        cursor.execute(
            "INSERT INTO employees (name, salary, age, location, bonus) VALUES (?, ?, ?, ?, ?)",
            employee
        )
    
    conn.commit()
    conn.close()
    
    print(f"Added {len(high_bonus_employees)} employees with high bonuses to the database.")
    print("Employee details:")
    for i, emp in enumerate(high_bonus_employees, 1):
        name, salary, age, location, bonus = emp
        percentage = (bonus / salary) * 100
        print(f"{i}. {name}: Salary ${salary}, Bonus ${bonus} ({percentage:.2f}% of salary)")


if __name__ == "__main__":
    main()
