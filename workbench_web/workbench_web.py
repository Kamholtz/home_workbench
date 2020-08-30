import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, Request, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every

from home_workbench.database import LoggingDatabase, Measurement
from home_workbench.spd3303c import SPD3303C, SPD3303CChannel
from home_workbench.workbench_helper import WorkbenchHelper


def get_full_path_from_cwd(path):
    root = os.path.dirname(os.path.realpath(__file__))
    return f"{root}\\{path}"


app = FastAPI()
templates_path = get_full_path_from_cwd("templates")
print(templates_path)
templates = Jinja2Templates(directory=templates_path)
ps = SPD3303C()
logging_database: LoggingDatabase = LoggingDatabase()

with open(get_full_path_from_cwd("measurements.json"), "r") as file:
    measurements = iter(json.loads(file.read()))

public_path = get_full_path_from_cwd("public")
app.mount("/public", StaticFiles(directory=public_path), name="public")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    last_update_time = datetime.now() - timedelta(minutes=30)
    while True:
        payload = next(measurements)

        latest_measurements: List[
            Measurement
        ] = logging_database.get_measurements_since_date(last_update_time)

        payload = [
            {
                "time": jsonable_encoder(m.d_datetime),
                "value": m.i_value,
                "measurement_type": m.i_measurement_type,
            }
            for m in latest_measurements
        ]

        last_update_time = datetime.now()
        await websocket.send_json(payload)
        await asyncio.sleep(1)


@app.on_event("startup")
@repeat_every(seconds=5)
def read_power_supply_and_insert() -> None:

    channels: List[SPD3303CChannel] = [ps.channel_1]

    for c in channels:
        meas = Measurement()
        meas.i_device_id = 1
        meas.i_channel_id = c.channel
        meas.i_measurement_type = 1
        meas.i_value = c.voltage
        meas.d_datetime = WorkbenchHelper.get_datetime_now_to_nearest_sec()
        logging_database.insert_measurement(meas)

        meas = Measurement()
        meas.i_device_id = 1
        meas.i_channel_id = c.channel
        meas.i_measurement_type = 2
        meas.i_value = c.current
        meas.d_datetime = WorkbenchHelper.get_datetime_now_to_nearest_sec()
        logging_database.insert_measurement(meas)


# @app.on_event("startup")
# @repeat_every(seconds=5)
def insert_fake_power_supply_data() -> None:
    new_measurement: Measurement = Measurement()
    new_measurement.i_measurement_type = 1
    new_measurement.i_device_id = 1
    new_measurement.i_channel_id = 1
    new_measurement.d_datetime = WorkbenchHelper.get_datetime_now_to_nearest_sec()
    new_measurement.i_value = WorkbenchHelper.get_float_with_variation(
        mid_point=5, max_variation=0.25, decimal_places=1
    )

    logging_database.insert_measurement(new_measurement)

    new_measurement = Measurement()
    new_measurement.i_measurement_type = 2
    new_measurement.i_device_id = 1
    new_measurement.i_channel_id = 1
    new_measurement.d_datetime = WorkbenchHelper.get_datetime_now_to_nearest_sec()
    new_measurement.i_value = WorkbenchHelper.get_float_with_variation(
        mid_point=0.100, max_variation=0.050, decimal_places=3
    )

    logging_database.insert_measurement(new_measurement)
