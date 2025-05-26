"""
C789 Control Example

This script demonstrates how to use the C789Control.
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.business_controls_framework.controls.C789.control import C789Control

data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                         '..', 'src', 'business_controls_framework',
                                         'controls', 'C789', 'data', 'sample.csv'))

if not os.path.exists(data_file):
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, 'w') as f:
        f.write("id,value\n")
        f.write("1,50\n")
        f.write("2,150\n")  # Exceeds threshold
        f.write("3,90\n")

control = C789Control(data_file=data_file)
result = control.run()

print(f"Control ID: {result.control_id}")
print(f"Passed: {result.passed}")
print("Reasons:")
for reason in result.reasons:
    print(f"  - {reason}")

if not result.passed:
    print("\nViolations:")
    for item in result.details.get("query_result", {}).get("results", []):
        value = item.get("value")
        if value is not None and float(value) > 100:
            print(f"  - ID {item.get('id')}: Value {value} exceeds threshold 100")
