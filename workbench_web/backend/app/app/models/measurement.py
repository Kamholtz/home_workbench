from sqlalchemy.ext.declarative import declarative_base

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
