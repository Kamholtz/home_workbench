import random as rand
from datetime import timedelta
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
    db.insert_measurement(measurement)

    assert measurement.i_id is not None

    measurement = Measurement()
    measurement.i_measurement_type = 2
    measurement.i_device_id = 1
    measurement.i_channel_id = 1
    measurement.d_datetime = WorkbenchHelper.GetDatetimeNowToNearestSecond()
    measurement.i_value = round(0.3 + rand.random() * 1, 1)
    db.insert_measurement(measurement)

    assert measurement.i_id is not None


def test_measurements_get_all_measurements() -> None:
    db = LoggingDatabase()
    measurements: List[Measurement] = db.get_all_measurements()

    assert len(measurements) > 0


def test_measurements_get_measurements_in_last_timedelta() -> None:
    db = LoggingDatabase()
    measurements: List[Measurement] = db.get_measurements_in_last_timedelta(
        period=timedelta(minutes=60)
    )

    assert len(measurements) > 0


def test_get_by_query() -> None:
    db = LoggingDatabase()
    result = db.get_by_query("public.measurements")

    assert len(result) > 0
