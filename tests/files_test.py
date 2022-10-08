import pandas as pd

from inline_sql import sql, sql_val


def test_weather():
    assert sql_val^ "SELECT COUNT() FROM 'tests/data/weather.csv'" == 1461  # fmt: skip
    pd.testing.assert_frame_equal(
        sql^ """
            SELECT weather, AVG(temp_max) as avg_temp FROM 'tests/data/weather.csv'
            WHERE weather IN ('rain', 'snow')
            GROUP BY weather
            ORDER BY weather ASC
        """,
        pd.DataFrame({
            "weather": ["rain", "snow"],
            "avg_temp": [12.584942, 5.504348],
        }),
    )  # fmt: skip


def test_disasters():
    assert sql_val^ "SELECT COUNT() FROM 'tests/data/disasters.csv'" == 803  # fmt: skip

    n = 50
    df = sql^ "SELECT * FROM 'tests/data/disasters.csv' LIMIT $n"  # fmt: skip
    assert isinstance(df, pd.DataFrame)
    assert sql_val^ "SELECT COUNT() FROM df" == 50  # fmt: skip
