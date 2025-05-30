"""
Example script for running the C123 control with SQLite database.

This script demonstrates how to use the C123 control with a SQLite database
instead of a CSV file.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C123.sql_control import C123SQLControl


def main():
    """Run the C123 control with SQLite database."""
    db_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src", "business_controls_framework", "controls", "C123", "data", "employees.db"
    )
    
    control = C123SQLControl(db_file)
    
    result = control.run()
    
    print(f"Control {result.control_id}: {'PASSED' if result.passed else 'FAILED'}")
    for reason in result.reasons:
        print(f"  - {reason}")
    
    if not result.passed:
        print("\nViolations:")
        for item in result.details["query_result"]["results"]:
            bonus = item.get("bonus")
            salary = item.get("salary")
            
            if bonus is not None and salary is not None and salary > 0:
                percentage = (bonus / salary) * 100
                
                if percentage > 20:
                    print(f"  - Employee {item.get('name')}: Bonus ${bonus} is {percentage:.2f}% of salary ${salary}")


if __name__ == "__main__":
    main()
