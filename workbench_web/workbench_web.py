import asyncio
import json
import os
import random as rand
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every

from home_workbench.database import LoggingDatabase, Measurement
from home_workbench.spd3303c import SPD3303C


def get_full_path_from_cwd(path):
    root = os.path.dirname(os.path.realpath(__file__))
    return f"{root}\\{path}"


app = FastAPI()
templates_path = get_full_path_from_cwd("templates")
print(templates_path)
templates = Jinja2Templates(directory=templates_path)
ps = SPD3303C()
logging_database = LoggingDatabase()

with open(get_full_path_from_cwd("measurements.json"), "r") as file:
    measurements = iter(json.loads(file.read()))


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(0.1)
        payload = next(measurements)
        now = datetime.now()
        now_rounded = now - timedelta(microseconds=now.microsecond)
        datetime_encoded = jsonable_encoder(now_rounded)
        payload = {
            "time": datetime_encoded,
            "current": ps.channel_1.current,
            "voltage": ps.channel_1.voltage,
        }
        await websocket.send_json(payload)


@app.on_event("startup")
@repeat_every(seconds=5)
def insert_fake_power_supply_data() -> None:
    now = datetime.now()

    new_measurement: Measurement = Measurement()
    # new_measurement.i_id = 3
    new_measurement.i_measurement_type = 1
    new_measurement.i_device_id = 1
    new_measurement.i_channel_id = 1
    # new_measurement.d_datetime = now
    new_measurement.i_value = rand.random() * 10

    logging_database.insert_measurement(new_measurement)

    new_measurement.i_measurement_type = 2
    new_measurement.i_device_id = 1
    new_measurement.i_channel_id = 1
    new_measurement.d_datetime = now
    new_measurement.i_value = rand.random() * 1

    logging_database.insert_measurement(new_measurement)
