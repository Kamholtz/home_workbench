from datetime import datetime, timedelta
from typing import List

import models.measurement
import schemas.measurement
import sqlalchemy as db
from db.database import Base, SessionLocal, engine
from db.workbench_helper import WorkbenchHelper
from models.measurement import Measurement
from sqlalchemy.orm import Session

from core.config import settings

class LoggingDatabase:

    def get_all_measurements(self, db: Session) -> List[Measurement]:
        measurements: List[Measurement] = db.query(Measurement).all()

        for meas in measurements:
            print(meas)

        return measurements

    # def get_by_query(self, query):
    #     fetchQuery = self.connection.execute(f"SELECT * FROM {query}")
    #     query_data = fetchQuery.fetchall()

    #     for data in query_data:
    #         print(data)

    #     return query_data

    def insert_measurement(
        self, db: Session, measurement: schemas.measurement.MeasurementCreate
    ) -> models.measurement.Measurement:

        db_measurement = models.measurement.Measurement(**measurement.dict())

        db.add(db_measurement)
        db.commit()
        db.refresh(db_measurement)

        print(db_measurement)

        return db_measurement

    def get_measurements_limit(self, db: Session, device_id: int, limit: int) -> List[Measurement]:
        db = Session(bind=self.connection)
        measurements: List[Measurement] = db.query(Measurement).filter(
            Measurement.i_device_id == device_id
        ).order_by(Measurement.d_datetime.desc()).limit(limit).all()

        return measurements

    def get_measurements_since_date(
        self, db: Session, since_date: datetime, device_id: int
    ) -> List[Measurement]:
        measurements: List[Measurement] = db.query(Measurement).filter(
            Measurement.d_datetime > since_date
        ).filter(Measurement.i_device_id == device_id).order_by(
            Measurement.d_datetime.asc()
        ).all()

        return measurements

    def get_measurements_in_last_timedelta(self, db: Session, period: timedelta, device_id: int):
        since_date = WorkbenchHelper.get_datetime_now_to_nearest_sec() - period
        return self.get_measurements_since_date(db, since_date, device_id)


# if __name__ == "__main__":
#     loggingDb = LoggingDatabase()
#     results = loggingDb.get_by_query("public.measurements")
#     results = loggingDb.get_all_measurements()
