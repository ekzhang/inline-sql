import duckdb
import pytest

from inline_sql import sql, sql_val


def test_basic_math():
    assert sql_val^ "SELECT 1 + 2" == 3  # fmt: skip
    assert sql_val^ "SELECT 1234567 * 2" == 2469134  # fmt: skip
    assert sql_val^ "SELECT POW(x, 2) FROM (SELECT 5 AS x)" == 25  # fmt: skip


def test_val_cardinality():
    assert sql_val^ "SELECT 1 WHERE 1 = 0" is None  # fmt: skip

    with pytest.raises(RuntimeError) as exc:
        sql_val^ "SELECT 1 UNION SELECT 2"  # fmt: skip
    assert "more than one row" in str(exc.value)

    with pytest.raises(RuntimeError) as exc:
        sql_val^ "SELECT 1 AS x, 2 AS y"  # fmt: skip
    assert "more than one column" in str(exc.value)


def test_invalid_query():
    with pytest.raises(ValueError):
        sql^ "INSERT INTO foo VALUES (1, 2)"  # fmt: skip
    with pytest.raises(ValueError):
        sql^ "SELECT 1; SELECT 2"  # fmt: skip
    with pytest.raises(NameError):
        sql^ "SELECT $x"  # fmt: skip
    with pytest.raises(duckdb.ParserException):
        sql^ "SELECT SELECT"  # fmt: skip


def test_query_df():
    df = sql^ "SELECT 1 AS x, 2 AS y"  # fmt: skip
    assert df.shape == (1, 2)
    assert df.iloc[0, 0] == 1
    assert df.iloc[0, 1] == 2
    assert list(df.columns) == ["x", "y"]


def test_params():
    x, y = 5, 6
    assert sql_val^ "SELECT $x + $y" == 11  # fmt: skip
    assert sql_val^ "SELECT $y + $x" == 11  # fmt: skip
    assert sql_val^ "SELECT $x + $x" == 10  # fmt: skip
    assert sql_val^ "SELECT $x + $x + $x" == 15  # fmt: skip
    assert sql_val^ "SELECT $x + $x + $x + $x" == 20  # fmt: skip
