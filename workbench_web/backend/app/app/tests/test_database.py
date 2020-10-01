from datetime import timedelta
from typing import List

from crud.measurement import LoggingDatabase
from db.workbench_helper import WorkbenchHelper
from models.measurement import Measurement
from schemas.measurement import MeasurementCreate


def test_create_tables() -> None:
    db = LoggingDatabase()
    db.create_tables()

    assert True


def test_measurements_insert() -> None:
    db = LoggingDatabase()
    measurement = MeasurementCreate(
        i_device_id=1,
        i_channel_id=1,
        i_measurement_type=1,
        i_value=WorkbenchHelper.get_float_with_variation(
            mid_point=5, max_variation=0.5, decimal_places=1
        ),
        d_datetime=WorkbenchHelper.get_datetime_now_to_nearest_sec(),
    )
    db_measurement = db.insert_measurement(measurement)

    assert db_measurement.i_id is not None

    measurement = MeasurementCreate(
        i_measurement_type=2,
        i_device_id=1,
        i_channel_id=1,
        d_datetime=WorkbenchHelper.get_datetime_now_to_nearest_sec(),
        i_value=WorkbenchHelper.get_float_with_variation(
            mid_point=0.300, max_variation=0.050, decimal_places=3
        ),
    )

    db_measurement = db.insert_measurement(measurement)
    assert db_measurement.i_id is not None


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
