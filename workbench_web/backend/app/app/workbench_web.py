import asyncio
from datetime import datetime, timedelta
from typing import List

import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi_utils.tasks import repeat_every
from workbench_web_helper import WorkbenchWebHelper

from home_workbench.database import LoggingDatabase, Measurement
from home_workbench.spd3303c import SPD3303C, SPD3303CChannel
from home_workbench.workbench_helper import WorkbenchHelper

# from fastapi.templating import Jinja2Templates


# https://github.com/encode/uvicorn/issues/358


app = FastAPI()
origins = ["http://localhost", "http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# templates_path = get_path_relative_to_this_module("templates")
# templates = Jinja2Templates(directory=templates_path)


ps: SPD3303C = WorkbenchWebHelper.get_power_supply()
logging_database: LoggingDatabase = LoggingDatabase()


@app.get("/greeting")
async def get_greeting():
    return {"greeting": "Hello World"}


@app.get("/")
def read_root(request: Request):
    index_path = "workbench_web/dist/index.html"
    return FileResponse(index_path, media_type="text/html")


@app.websocket("/measurements")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    last_update_time = datetime.now() - timedelta(minutes=30)
    while True:
        latest_measurements: List[
            Measurement
        ] = logging_database.get_measurements_since_date(last_update_time)

        if latest_measurements:
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
@repeat_every(seconds=3)
def read_power_supply_and_insert() -> None:
    global ps
    if ps is None:
        ps = WorkbenchWebHelper.get_power_supply()
        return
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


@app.on_event("startup")
@repeat_every(seconds=5)
def insert_fake_power_supply_data() -> None:

    if ps is not None:
        return

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


if __name__ == "__main__":
    uvicorn.run("workbench_web:app", host="localhost", port=5000, reload=True)
