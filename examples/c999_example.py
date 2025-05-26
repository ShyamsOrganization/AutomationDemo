"""
C999 Control Example

This script demonstrates how to use the C999Control.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C999.control import C999Control

data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', 'src', 'business_controls_framework',
                                         'controls', 'C999', 'data', 'account_balances.csv'))

control = C999Control(data_file=data_file)
result = control.run()

print(f"Control ID: {result.control_id}")
print(f"Description: Check customer account balances")
print(f"Passed: {result.passed}")
print("Reasons:")
for reason in result.reasons:
    print(f"  - {reason}")

if not result.passed:
    print("\nViolations:")
    for item in result.details.get("query_result", {}).get("results", []):
        print(f"  - ID {item.get('id')}: {item}")
