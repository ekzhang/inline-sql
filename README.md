# Inline SQL

[![PyPI - Version](https://img.shields.io/pypi/v/inline-sql.svg)](https://pypi.org/project/inline-sql)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/inline-sql.svg)](https://pypi.org/project/inline-sql)

A simple embedded language for running inline SQL in Python programs.

```python
import pandas as pd
from inline_sql import sql, sql_val


def head_data(count: int) -> pd.DataFrame:
    return sql^ "SELECT * FROM 'cars.csv' LIMIT $count"


cars = head_data(50)

origin_counts = sql^ """
    SELECT origin, COUNT() FROM cars
    GROUP BY origin
    ORDER BY count DESC
"""
print(origin_counts)

most_common = origin_counts.origin[0]
print(sql_val^ """
    SELECT AVG(horsepower) FROM cars
    WHERE origin = $most_common
""")
```

Operations in the `inline_sql` library directly use an in-memory database. You can access local datasets (pandas frames), CSV files, and interpolate variables seamlessly into queries. Internally, this is implemented as a small wrapper around [DuckDB](https://duckdb.org/).

## Installation

Supports Python 3.7+, tested on all major operating systems.

```console
pip install inline-sql
```

## Usage

The exported `sql` and `sql_val` variables are magic objects that can be used to run queries. Queries can read from local dataframes by name, and they can embed parameters using dollar-sign notation.

```python
>>> from inline_sql import sql, sql_val

>>> sql_val^ "SELECT 1 + 1"
2

>>> x = 5

>>> sql_val^ "SELECT 2 * $x"
10

>>> sql^ "SELECT * FROM 'disasters.csv' LIMIT 5"
                  Entity  Year   Deaths
0  All natural disasters  1900  1267360
1  All natural disasters  1901   200018
2  All natural disasters  1902    46037
3  All natural disasters  1903     6506
4  All natural disasters  1905    22758

>>> def total_deaths(entity: str) -> float:
...     return sql_val^ "SELECT SUM(deaths) FROM disasters WHERE Entity = $entity"
...

>>> total_deaths("Drought")
11731294.0

>>> total_deaths("Earthquake")
2576801.0
```

You can run any SQL query as described in the [DuckDB documentation](https://duckdb.org/docs/guides/).

## Acknowledgements

Created by Eric Zhang ([@ekzhang1](https://twitter.com/ekzhang1)). Licensed under the [MIT license](LICENSE).
