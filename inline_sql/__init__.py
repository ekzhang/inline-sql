from typing import Any

import pandas as pd

from ._src.executor import InlineSQL

__all__ = ["sql", "sql_val"]


sql: InlineSQL[pd.DataFrame] = InlineSQL(scalar=False)
sql_val: InlineSQL[Any] = InlineSQL(scalar=True)
