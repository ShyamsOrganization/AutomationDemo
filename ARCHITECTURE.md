# Business Controls Framework Architecture

## Overview

The Business Controls Framework is designed to automate the testing of business controls. The framework allows for defining controls that query data sources and apply assertions to verify that the data meets specific criteria.

## Directory Structure

The framework is organized by control, with each control having its own directory containing all related files:

```
src/business_controls_framework/
├── api/                      # API components
├── controls/                 # Controls directory
│   ├── C123/                 # C123 control directory
│   │   ├── __init__.py       # Package initialization
│   │   ├── control.py        # C123 control implementation
│   │   ├── control_v2.py     # C123 V2 control implementation
│   │   ├── assertion.py      # MaxPercentageAssertion for C123
│   │   ├── query.py          # SimpleQuery for C123
│   │   └── data/             # C123-specific data files
│   │       ├── employees.csv
│   │       └── employees_large.csv
│   ├── C456/                 # C456 control directory
│   │   ├── __init__.py       # Package initialization
│   │   ├── control.py        # C456 control implementation
│   │   ├── assertion.py      # RangeAssertion for C456
│   │   ├── query.py          # SimpleQuery for C456
│   │   └── data/             # C456-specific data files
│   │       └── loans.csv
│   ├── base_control.py       # Base class for original controls
│   └── base_control_v2.py    # Base class for new controls
├── data_connectors/          # Data connector components
├── query_engine/             # Shared query engine components
├── assertion_engine/         # Shared assertion engine components
├── main.py                   # Main entry point (original architecture)
└── main_v2.py                # Main entry point (new architecture)
```

## Architecture Components

The framework is built around the following key components:

### Data Connectors

Data connectors provide a standardized interface for accessing different types of data sources:

- `BaseConnector`: Abstract base class for all data connectors
- `CSVConnector`: Connector for CSV files
- `SQLConnector`: Connector for SQL databases

### Query Engine

The query engine provides functionality for building and executing queries against data sources:

- `BaseQuery`: Abstract base class for all queries
- Each control has its own query implementation in its directory

### Assertion Engine

The assertion engine provides functionality for evaluating assertions against data:

- `BaseAssertion`: Abstract base class for all assertions
- Each control has its own assertion implementation in its directory

### Controls

Controls combine queries and assertions to verify that data meets specific criteria:

- `BaseControl`: Original base class for all controls (using the centralized assertion registry)
- `BaseControlV2`: Enhanced base class for all controls with custom assertions
- Each control has its own directory with implementation files

### API

The API provides a standardized interface for running controls and retrieving results:

- `ControlAPI`: API for running control tests and retrieving results

## Control-Assertion Mapping

Each control is associated with specific assertion types based on its business requirements. The following table shows the mapping between controls and assertions:

| Control ID | Control Purpose | Assertion Type | Input Data |
|------------|-----------------|----------------|------------|
| C123 | Employee Bonus Check | MaxPercentageAssertion | Employee data (salary, bonus) |
| C456 | Interest Rate Check | RangeAssertion | Loan data (interest rates) |

### Naming Conventions

To maintain clarity and consistency, the following naming conventions are recommended:

1. **Control Directories**: `[ControlID]` (e.g., `C123`, `C456`)
2. **Control Implementation**: `control.py` in the control's directory
3. **Assertion Implementation**: `assertion.py` in the control's directory
4. **Query Implementation**: `query.py` in the control's directory
5. **Test Classes**: `Test[ControlID]` (e.g., `TestC123`, `TestC456`)
6. **Data Files**: Stored in the `data/` subdirectory of each control

### Documentation Requirements

Each control class should include:

1. A class-level docstring describing the control's purpose
2. Documentation of which assertion type it uses and why
3. Clear description of the input data requirements
4. Explanation of the parameters used for assertion evaluation

## Architecture Evolution

The framework has evolved from a centralized assertion registry to a more flexible architecture that allows controls to define their own custom assertions:

### Original Architecture

In the original architecture, all assertions were registered in a central `AssertionEvaluator` class. Controls would use this evaluator to run assertions by name.

```
Control -> AssertionEvaluator -> Assertion Functions
```

### New Architecture

In the new architecture, controls can define their own custom assertions by implementing the `BaseAssertion` interface. This allows for more flexibility and better separation of concerns.

```
Control -> Custom Assertion Implementation
```

The new architecture also introduces a similar pattern for queries, allowing controls to define their own custom queries by implementing the `BaseQuery` interface.

```
Control -> Custom Query Implementation -> Data Connector
```

### Control-Specific Organization

The latest evolution organizes all files related to a control in its own directory:

```
Control Directory/
├── control.py        # Control implementation
├── assertion.py      # Assertion implementation
├── query.py          # Query implementation
└── data/             # Control-specific data files
```

This organization makes it easier to manage thousands of controls, as each control's components are grouped together.

## Adding New Controls

To add a new control with its own query and assertion logic:

1. Create a new directory under `controls/` with the control ID (e.g., `C789`)
2. Create the following files in the new directory:
   - `__init__.py`: Package initialization
   - `control.py`: Control implementation extending `BaseControlV2`
   - `assertion.py`: Custom assertion implementation
   - `query.py`: Custom query implementation
   - `data/`: Directory for control-specific data files
3. Implement the control class with the required methods:
   - `create_query()`: Returns the appropriate query for this control
   - `create_assertion()`: Returns the appropriate assertion for this control
   - `get_assertion_params()`: Provides the parameters for the assertion
4. Document the control-assertion relationship in the class docstring

Example:
```python
# controls/C789/control.py
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.csv_connector import CSVConnector
from .query import SimpleQuery
from .assertion import RangeAssertion

class C789Control(BaseControlV2):
    """
    Control for checking customer credit limits.
    
    This control uses the RangeAssertion to verify that customer
    credit limits are appropriate based on their credit score.
    """
    
    def create_query(self):
        connector = CSVConnector(self.data_file)
        return SimpleQuery(connector)
        
    def create_assertion(self):
        return RangeAssertion()
        
    def get_assertion_params(self):
        return {
            "field": "credit_limit",
            "min_value": 1000,
            "max_value": 50000
        }
```

## Backward Compatibility

The framework maintains backward compatibility with the original architecture, allowing existing controls to continue working without modification. New controls can take advantage of the more flexible architecture and control-specific organization.
