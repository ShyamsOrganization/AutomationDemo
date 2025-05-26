"""
Interest Rate Control Example

This script demonstrates how to use the C456Control to check interest rates.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C456 import C456Control

data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', 'tests', 'data', 'loans.csv'))

control = C456Control(data_file=data_file)
result = control.run()

print(f"Control ID: {result.control_id}")
print(f"Passed: {result.passed}")
print("Reasons:")
for reason in result.reasons:
    print(f"  - {reason}")

if not result.passed:
    print("\nViolations:")
    for item in result.details.get("query_result", {}).get("results", []):
        interest_rate = item.get("interest_rate")
        if interest_rate is not None:
            if float(interest_rate) < 2.0 or float(interest_rate) > 15.0:
                print(f"  - Loan {item.get('loan_id')}: Interest rate {interest_rate}% is outside allowed range (2-15%)")
