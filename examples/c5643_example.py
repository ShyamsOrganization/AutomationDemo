"""
Example script for running the C5643 control.

This script demonstrates how to use the C5643 control to check
that no employee has a salary exceeding 100k USD.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C5643.control import C5643Control


def main():
    """Run the C5643 control with SQLite database."""
    db_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src", "business_controls_framework", "controls", "C123", "data", "employees.db"
    )
    
    control = C5643Control(db_file)
    
    result = control.run()
    
    print(f"Control {result.control_id}: {'PASSED' if result.passed else 'FAILED'}")
    for reason in result.reasons:
        print(f"  - {reason}")
    
    if not result.passed:
        print("\nViolations:")
        for item in result.details["query_result"]["results"]:
            salary = item.get("salary")
            
            if salary is not None and salary > 100000:
                print(f"  - Employee {item.get('name')}: Salary ${salary} exceeds the 100k USD threshold")


if __name__ == "__main__":
    main()
