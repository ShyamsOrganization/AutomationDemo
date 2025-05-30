# Using SQLite with Business Controls Framework

This document provides guidance on using SQLite databases with the Business Controls Framework.

## Overview

The Business Controls Framework supports both CSV files and SQLite databases as data sources for controls. SQLite provides several advantages:

- Support for complex SQL queries
- Better performance for large datasets
- Ability to enforce data types and constraints
- No separate server setup required

## Directory Structure

Each control should have its own SQLite database file in its control-specific directory:

```
src/business_controls_framework/
├── controls/
│   ├── C123/                 # Control using CSV
│   │   ├── data/
│   │   │   └── employees.csv
│   ├── C999/                 # Control using SQLite
│   │   ├── data/
│   │   │   └── accounts.db   # SQLite database file
```

## Creating a SQLite Database

You can create a SQLite database for a control in two ways:

### 1. Using the Enhanced SQL Connector

```python
from src.business_controls_framework.data_connectors.enhanced_sql_connector import EnhancedSQLConnector

# Create a connector
connector = EnhancedSQLConnector("path/to/database.db")

# Create a table
connector.create_table(
    "table_name",
    [
        ("column1", "TEXT"),
        ("column2", "INTEGER"),
        ("column3", "REAL")
    ]
)

# Insert data
connector.insert_data(
    "table_name",
    [
        {"column1": "value1", "column2": 123, "column3": 45.6},
        {"column1": "value2", "column2": 789, "column3": 12.3}
    ]
)
```

### 2. Converting from CSV

```python
from src.business_controls_framework.utils.sqlite_utils import csv_to_sqlite

# Convert a CSV file to a SQLite database
csv_to_sqlite(
    "path/to/data.csv",
    "path/to/database.db",
    "table_name"
)
```

## Creating a Control with SQLite

To create a control that uses a SQLite database:

1. Create a control class that uses the `EnhancedSQLConnector`:

```python
from ...controls.base_control_v2 import BaseControlV2
from ...data_connectors.enhanced_sql_connector import EnhancedSQLConnector
from .query import SQLQuery
from .assertion import YourAssertion

class YourControl(BaseControlV2):
    def create_query(self):
        connector = EnhancedSQLConnector(self.data_file)
        return SQLQuery(connector)
```

2. Create a query class that uses SQL:

```python
from ...query_engine.base_query import BaseQuery

class SQLQuery(BaseQuery):
    def __init__(self, connector, query_string="SELECT * FROM your_table"):
        super().__init__(connector)
        self.query_string = query_string
    
    def execute(self):
        results = self.connector.execute_query(self.query_string)
        return {"results": results}
```

## Example

See the C999 control for a complete example of using SQLite with the Business Controls Framework:

- `src/business_controls_framework/controls/C999/control.py`
- `src/business_controls_framework/controls/C999/query.py`
- `src/business_controls_framework/controls/C999/data/setup_database.py`
- `examples/sqlite_control_example.py`
