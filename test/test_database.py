import random as rand
from typing import List

from home_workbench.database import LoggingDatabase, Measurement
from home_workbench.workbench_helper import WorkbenchHelper


def test_create_table() -> None:
    db = LoggingDatabase()
    db.create_table()

    assert True


def test_measurements_insert() -> None:
    db = LoggingDatabase()
    measurement = Measurement()
    measurement.i_device_id = 1
    measurement.i_channel_id = 1
    measurement.i_measurement_type = 1
    measurement.i_value = round(4.75 + rand.random() * 5, 1)
    measurement.d_datetime = WorkbenchHelper.GetDatetimeNowToNearestSecond()
    db.add_measurement(measurement)

    # assert measurement.i_id != None

    measurement = Measurement()
    measurement.i_measurement_type = 2
    measurement.i_device_id = 1
    measurement.i_channel_id = 1
    measurement.d_datetime = WorkbenchHelper.GetDatetimeNowToNearestSecond()
    measurement.i_value = round(0.3 + rand.random() * 1, 1)
    db.add_measurement(measurement)

    # assert measurement.i_id != None


def test_measurements_get_all_measurements() -> None:
    db = LoggingDatabase()
    measurements: List[Measurement] = db.fetch_all_measurements()

    assert len(measurements) > 0


def test_fetch_by_query() -> None:
    db = LoggingDatabase()
    result = db.fetch_by_query("public.measurements")

    assert len(result) > 0
