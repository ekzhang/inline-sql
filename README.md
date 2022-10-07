# Inline SQL

[![PyPI - Version](https://img.shields.io/pypi/v/inline-sql.svg)](https://pypi.org/project/inline-sql)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/inline-sql.svg)](https://pypi.org/project/inline-sql)

An engine for inline SQL in any Python program.

```python
import pandas as pd
from inline_sql import sql


def head_data(count: int) -> pd.DataFrame:
    return sql << "SELECT * FROM 'cars.csv' LIMIT $count"


cars = head_data(50)

origin_counts = sql << """
    SELECT origin, COUNT(*) FROM $cars
    GROUP BY origin
    ORDER BY count DESC
"""
print(origin_counts)

most_common = origin_counts.origin[0]
print(sql << """
    SELECT AVG(horsepower) FROM $cars
    WHERE origin = $most_common
""")
```

Operates directly on an in-memory database: access local variables (pandas frames), CSV files, and interpolate values into queries.

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install inline-sql
```

## Contributions

Contributions are appreciated, especially in the following areas:

- Additional query engines
- File format support (CSV, Parquet, Arrow)
- Support for dataframe libraries (e.g., Polars)
- Distributed computing (Ray, Dask)
- Documentation

## License

`inline-sql` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
