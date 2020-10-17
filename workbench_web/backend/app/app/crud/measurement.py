from datetime import datetime, timedelta
from typing import List

import models.measurement
import schemas.measurement
import sqlalchemy as db
from db.database import Base
from db.workbench_helper import WorkbenchHelper
from models.measurement import Measurement
from sqlalchemy.orm import Session


class LoggingDatabase:
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine(
        "postgresql://read_write:simplepass1098@localhost:5432/logging", echo=False
    )

    def __init__(self):
        self.connection = self.engine.connect()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_all_measurements(self) -> List[Measurement]:
        self.session = Session(bind=self.connection)
        measurements: List[Measurement] = self.session.query(Measurement).all()

        for meas in measurements:
            print(meas)

        return measurements

    def get_by_query(self, query):
        fetchQuery = self.connection.execute(f"SELECT * FROM {query}")
        query_data = fetchQuery.fetchall()

        for data in query_data:
            print(data)

        return query_data

    def insert_measurement(
        self, measurement: schemas.measurement.MeasurementCreate
    ) -> models.measurement.Measurement:
        session = Session(bind=self.connection)
        db_measurement = models.measurement.Measurement(**measurement.dict())
        session.add(db_measurement)
        session.commit()
        session.refresh(db_measurement)

        return db_measurement

    def get_measurements_limit(self, device_id: int, limit: int) -> List[Measurement]:
        session = Session(bind=self.connection)
        measurements: List[Measurement] = session.query(Measurement).filter(
            Measurement.i_device_id == device_id
        ).order_by(Measurement.d_datetime.desc()).limit(limit).all()

        return measurements

    def get_measurements_since_date(
        self, since_date: datetime, device_id: int
    ) -> List[Measurement]:
        session = Session(bind=self.connection)
        measurements: List[Measurement] = session.query(Measurement).filter(
            Measurement.d_datetime > since_date
        ).filter(Measurement.i_device_id == device_id).order_by(
            Measurement.d_datetime.asc()
        ).all()

        return measurements

    def get_measurements_in_last_timedelta(self, period: timedelta, device_id: int):
        since_date = WorkbenchHelper.get_datetime_now_to_nearest_sec() - period
        return self.get_measurements_since_date(since_date, device_id)


if __name__ == "__main__":
    loggingDb = LoggingDatabase()
    results = loggingDb.get_by_query("public.measurements")
    results = loggingDb.get_all_measurements()
