from home_workbench.database import LoggingDatabase


def test_fetch_by_query() -> None:
    db = LoggingDatabase()
    result = db.fetch_by_query("public.measurements")
    assert len(result) > 0
