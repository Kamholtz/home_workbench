from home_workbench.database import LoggingDatabase, Measurement
from home_workbench.workbench_helper import WorkbenchHelper


def test_create_table() -> None:
    db = LoggingDatabase()
    db.create_table()


def test_measurements_insert() -> None:
    db = LoggingDatabase()
    measurement = Measurement()
    measurement.i_device_id = 1
    measurement.i_channel_id = 1
    measurement.i_measurement_type = 1
    measurement.i_value = 1.2
    measurement.d_datetime = WorkbenchHelper.GetDatetimeNowToNearestSecond()

    db.add_measurement(measurement)


def test_fetch_by_query() -> None:
    db = LoggingDatabase()
    result = db.fetch_by_query("public.measurements")
    assert len(result) > 0
