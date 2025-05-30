"""
Example script for running the C7890 control.

This script demonstrates how to use the C7890 control to check
that no employee has a bonus exceeding 30% of their salary.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C7890.control import C7890Control


def main():
    """Run the C7890 control with SQLite database."""
    db_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src", "business_controls_framework", "controls", "C123", "data", "employees.db"
    )
    
    control = C7890Control(db_file)
    
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
                if percentage > 30:
                    print(f"  - Employee {item.get('name')}: Bonus ${bonus} is {percentage:.2f}% of salary ${salary}")


if __name__ == "__main__":
    main()
