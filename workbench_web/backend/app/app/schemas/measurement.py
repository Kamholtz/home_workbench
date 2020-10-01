from datetime import datetime

from pydantic import BaseModel


class MeasurementBase(BaseModel):
    i_device_id: int
    i_channel_id: int
    i_measurement_type: int
    i_value: float
    d_datetime: datetime


class MeasurementCreate(MeasurementBase):
    pass


class Measurement(MeasurementBase):
    i_id: int

    class Config:
        orm_mode = True
