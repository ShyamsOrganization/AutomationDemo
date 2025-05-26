# Business Controls Framework Architecture

## Overview

The Business Controls Framework is designed to automate the testing of business controls. The framework allows for defining controls that query data sources and apply assertions to verify that the data meets specific criteria.

## Architecture

The framework is built around the following key components:

### Data Connectors

Data connectors provide a standardized interface for accessing different types of data sources:

- `BaseConnector`: Abstract base class for all data connectors
- `CSVConnector`: Connector for CSV files
- `SQLConnector`: Connector for SQL databases

### Query Engine

The query engine provides functionality for building and executing queries against data sources:

- `BaseQuery`: Abstract base class for all queries
- `SimpleQuery`: A simple query implementation that passes a query string to a connector

### Assertion Engine

The assertion engine provides functionality for evaluating assertions against data:

- `BaseAssertion`: Abstract base class for all assertions
- `MaxPercentageAssertion`: Assertion for checking that one value is not more than a percentage of another value
- `RangeAssertion`: Assertion for checking that values are within a specified range

### Controls

Controls combine queries and assertions to verify that data meets specific criteria:

- `BaseControl`: Original base class for all controls (using the centralized assertion registry)
- `BaseControlV2`: Enhanced base class for all controls with custom assertions
- `C123Control`: Control for checking employee bonuses (using the original architecture)
- `C123ControlV2`: Control for checking employee bonuses (using the new architecture)
- `C456Control`: Control for checking interest rates (using the new architecture)

### API

The API provides a standardized interface for running controls and retrieving results:

- `ControlAPI`: API for running control tests and retrieving results

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

## Backward Compatibility

The framework maintains backward compatibility with the original architecture, allowing existing controls to continue working without modification. New controls can take advantage of the more flexible architecture.
