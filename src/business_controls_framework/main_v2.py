"""
Main module V2 for the Business Controls Testing Automation Framework.

This module provides the main entry point for running the framework with the new architecture.
"""
import os
import argparse
import json
import importlib
import pkgutil
from typing import Dict, Any, List

from .api.control_api import ControlAPI
from .controls.C123.control import C123Control
from .controls.C123.control_v2 import C123ControlV2
from .controls.C123.sql_control import C123SQLControl
from .controls.C456.control import C456Control
from .controls.C789.control import C789Control
from .controls.C999.control import C999Control
from .controls.C5643.control import C5643Control


def discover_controls():
    """
    Automatically discover all control modules in the controls directory.
    
    Returns:
        List of control module names
    """
    controls_pkg = importlib.import_module("src.business_controls_framework.controls")
    control_modules = []
    
    for _, name, is_pkg in pkgutil.iter_modules(controls_pkg.__path__):
        if is_pkg and name.startswith("C"):
            control_modules.append(name)
            
    return control_modules


def main() -> None:
    """Main entry point for the framework."""
    parser = argparse.ArgumentParser(description="Business Controls Testing Automation Framework")
    parser.add_argument("--control", help="ID of the control to run")
    parser.add_argument("--data-dir", default="./tests/data", help="Directory containing data files")
    parser.add_argument("--output", help="Output file for results (JSON format)")
    parser.add_argument("--discover", action="store_true", help="Automatically discover and register all controls")
    args = parser.parse_args()
    
    api = ControlAPI()
    
    c123_data_dir = os.path.join(os.path.dirname(__file__), "controls", "C123", "data")
    c456_data_dir = os.path.join(os.path.dirname(__file__), "controls", "C456", "data")
    c789_data_dir = os.path.join(os.path.dirname(__file__), "controls", "C789", "data")
    c999_data_dir = os.path.join(os.path.dirname(__file__), "controls", "C999", "data")
    c5643_data_dir = os.path.join(os.path.dirname(__file__), "controls", "C5643", "data")
    
    api.register_control(C123SQLControl(
        data_file=os.path.join(c123_data_dir, "employees.db"),
        control_id="C123",
        description="Check that employee bonuses are not more than 20% of salary (SQLite version)"
    ))
    
    api.register_control(C123Control(
        data_file=os.path.join(c123_data_dir, "employees.csv"),
        control_id="C123_CSV",
        description="Check that employee bonuses are not more than 20% of salary (CSV version)"
    ))
    
    api.register_control(C123ControlV2(
        data_file=os.path.join(c123_data_dir, "employees.csv"),
        control_id="C123_V2",
        description="Check that employee bonuses are not more than 20% of salary (new architecture)"
    ))
    
    api.register_control(C456Control(
        data_file=os.path.join(c456_data_dir, "loans.csv"),
        control_id="C456",
        description="Check that interest rates are within the allowed range (2% to 15%)"
    ))
    
    api.register_control(C789Control(
        data_file=os.path.join(c789_data_dir, "customer_credit.csv"),
        control_id="C789",
        description="Check customer credit scores are within acceptable range"
    ))
    
    api.register_control(C999Control(
        data_file=os.path.join(c999_data_dir, "accounts.db"),
        control_id="C999",
        description="Check customer account balances are within acceptable limits"
    ))
    
    api.register_control(C5643Control(
        data_file=os.path.join(c123_data_dir, "employees.db"),
        control_id="C5643",
        description="Check that no employee has a salary exceeding 100k USD"
    ))
    
    if args.discover:
        control_modules = discover_controls()
        print(f"Discovered control modules: {control_modules}")
    
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
