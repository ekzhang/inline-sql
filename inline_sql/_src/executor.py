import inspect
from typing import Generic, TypeVar

from .runtime import run_query

T = TypeVar("T")


class InlineSQL(Generic[T]):
    """A magic object that lets you run inline SQL queries.

    ### Usage

    ```
    from inline_sql import sql, sql_val

    sql_val^ "SELECT 1 + 1"  # => 2
    sql_val^ "SELECT COUNT() FROM 'disasters.csv'"  # => 803

    n = 50
    df = sql^ "SELECT * FROM 'disasters.csv' LIMIT $n"  # => pd.DataFrame({...})
    sql_val^ "SELECT COUNT() FROM df"  # => 50
    ```
    """

    def __init__(self, scalar: bool) -> None:
        self.scalar = scalar

    def __xor__(self, query: str) -> T:
        """Run an inline SQL query."""
        frame = inspect.currentframe()
        try:
            f_locals, f_globals = frame.f_back.f_locals, frame.f_back.f_globals
            context = {**f_globals, **f_locals}
        finally:
            del frame

        df = run_query(query, context)
        if self.scalar:
            if len(df) > 1:
                raise RuntimeError("Scalar query returned more than one row.")
            if len(df.columns) > 1:
                raise RuntimeError("Scalar query returned more than one column.")
            return None if df.empty else df.iloc[0, 0]  # type: ignore
        else:
            return df  # type: ignore
