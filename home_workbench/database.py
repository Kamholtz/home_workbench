from datetime import datetime, timedelta
from typing import List

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from home_workbench.workbench_helper import WorkbenchHelper

from sqlalchemy import (  # MetaData,; Sequence,; String,; Table,
    Column,
    DateTime,
    Float,
    Integer,
)

# https://itnext.io/sqlalchemy-orm-connecting-to-postgresql-from-scratch-create-fetch-update-and-delete-a86bc81333dc
Base = declarative_base()


class Measurement(Base):
    """ Model for measurement data. """

    __tablename__ = "measurements"
    i_id = Column(Integer, primary_key=True, autoincrement=True)
    i_device_id = Column(Integer)
    i_channel_id = Column(Integer)
    i_measurement_type = Column(Integer)
    i_value = Column(Float)
    d_datetime = Column(DateTime)

    def __repr__(self):
        return f"<Measurement(i_id={self.i_id}, i_device_id={self.i_device_id}, i_channel_id={self.i_channel_id}, i_measurement_type={self.i_measurement_type}, i_value={self.i_value}, d_datetime={self.d_datetime})>"


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

    def insert_measurement(self, measurement: Measurement):
        session = Session(bind=self.connection)
        session.add(measurement)
        session.commit()

    def get_measurements_since_date(self, since_date: datetime) -> List[Measurement]:
        session = Session(bind=self.connection)
        measurements: List[Measurement] = session.query(Measurement).filter(
            Measurement.d_datetime > since_date
        ).all()

        return measurements

    def get_measurements_in_last_timedelta(self, period: timedelta):
        since_date = WorkbenchHelper.get_datetime_now_to_nearest_sec() - period
        return self.get_measurements_since_date(since_date)


if __name__ == "__main__":
    loggingDb = LoggingDatabase()
    results = loggingDb.get_by_query("public.measurements")
    results = loggingDb.get_all_measurements()
