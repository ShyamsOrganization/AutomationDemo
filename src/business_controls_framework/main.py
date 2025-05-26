"""
Main module for the Business Controls Testing Automation Framework.

This module provides the main entry point for running the framework.
"""
import os
import argparse
import json
from typing import Dict, Any, List

from .api.control_api import ControlAPI
from .controls.C123 import C123Control


def main() -> None:
    """Main entry point for the framework."""
    parser = argparse.ArgumentParser(description="Business Controls Testing Automation Framework")
    parser.add_argument("--control", help="ID of the control to run")
    parser.add_argument("--data-dir", default="./tests/data", help="Directory containing data files")
    parser.add_argument("--output", help="Output file for results (JSON format)")
    args = parser.parse_args()
    
    api = ControlAPI()
    
    api.register_control(C123Control(
        data_file=os.path.join(args.data_dir, "employees.csv")
    ))
    
    api.register_control(C123Control(
        data_file=os.path.join(args.data_dir, "employees_large.csv"),
        control_id="C123_LARGE",
        description="Check that employee bonuses are not more than 20% of salary (large dataset)"
    ))
    
    if args.control:
        results = [api.run_control(args.control)]
    else:
        results = api.run_all_controls()
    
    for result in results:
        print(f"Control {result.control_id}: {'PASSED' if result.passed else 'FAILED'}")
        for reason in result.reasons:
            print(f"  - {reason}")
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(
                [
                    {
                        "control_id": r.control_id,
                        "passed": r.passed,
                        "reasons": r.reasons,
                        "details": r.details
                    }
                    for r in results
                ],
                f,
                indent=2
            )


if __name__ == "__main__":
    main()
