import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

import uvicorn
from crud.measurement import LoggingDatabase
from db.spd3303c import SPD3303C, SPD3303CChannel
from db.workbench_helper import WorkbenchHelper
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi_utils.tasks import repeat_every
from models.measurement import Measurement
from schemas.measurement import MeasurementCreate
from websockets import ConnectionClosed, ConnectionClosedError, ConnectionClosedOK
from workbench_web_helper import WorkbenchWebHelper

# from fastapi.templating import Jinja2Templates
# https://github.com/encode/uvicorn/issues/358


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://192.168.15.10",
    "http://192.168.15.10:8080",
    "http://192.168.1.20",
    "http://192.168.1.20:8080",
    "http://192.168.1.*",
    "http://192.168.1.*:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# templates_path = get_path_relative_to_this_module("templates")
# templates = Jinja2Templates(directory=templates_path)


ps: Optional[SPD3303C] = WorkbenchWebHelper.get_power_supply()
logging_database: LoggingDatabase = LoggingDatabase()


@app.get("/greeting")
async def get_greeting():
    return {"greeting": "Hello World"}


@app.get("/")
def read_root(request: Request):
    index_path = "workbench_web/dist/index.html"
    return FileResponse(index_path, media_type="text/html")


@app.post("/measurements")
async def create_measurement(measurement: MeasurementCreate) -> Measurement:

    if measurement.d_datetime is None:
        measurement.d_datetime = WorkbenchHelper.get_datetime_now_to_nearest_sec()

    print(measurement)
    return logging_database.insert_measurement(measurement)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            print("WebSocket was already removed")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)


measurements_manager: ConnectionManager = ConnectionManager()
channel_status_manager: ConnectionManager = ConnectionManager()


LAST_STATUS = None
LAST_STATUS_PAYLOAD = None
LAST_SOURCE_VOLTAGES: List[float] = [0] * 2
LAST_SOURCE_CURRENTS: List[float] = [0] * 2


@app.websocket("/channelstatus")
async def channel_status_endpoint(websocket: WebSocket):

    await channel_status_manager.connect(websocket)
    if LAST_STATUS_PAYLOAD is not None:
        await websocket.send_json(LAST_STATUS_PAYLOAD)

    try:
        while True:
            data = await websocket.receive_json()
            print(data)

    except (
        WebSocketDisconnect,
        ConnectionClosedOK,
        ConnectionClosed,
        ConnectionClosedError,
    ):
        measurements_manager.disconnect(websocket)


@app.websocket("/measurements")
async def websocket_endpoint(websocket: WebSocket):
    await measurements_manager.connect(websocket)

    last_update_time = datetime.now() - timedelta(minutes=30)
    try:
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
                        "channel": 1,
                    }
                    for m in latest_measurements
                ]

                last_update_time = datetime.now()
                await websocket.send_json(payload)

            await asyncio.sleep(1)

    except (
        WebSocketDisconnect,
        ConnectionClosedOK,
        ConnectionClosed,
        ConnectionClosedError,
    ):
        measurements_manager.disconnect(websocket)


@app.on_event("startup")
@repeat_every(seconds=3, raise_exceptions=True)
async def read_power_supply_and_insert() -> None:
    global ps
    global LAST_STATUS_PAYLOAD, LAST_STATUS, LAST_SOURCE_CURRENTS, LAST_SOURCE_VOLTAGES
    global channel_status_manager
    if ps is None:
        ps = WorkbenchWebHelper.get_power_supply()
        return

    status = ps.status

    channels: List[SPD3303CChannel] = [ps.channel_1, ps.channel_2]

    source_voltages = [c.source_voltage for c in channels]
    source_currents = [c.source_current for c in channels]

    if (
        LAST_STATUS is None
        or status != LAST_STATUS
        or source_voltages != LAST_SOURCE_VOLTAGES
        or source_currents != LAST_SOURCE_CURRENTS
    ):
        payload = [
            {
                "channel": 1,
                "supply_mode": status.channel_1_supply_mode.value,
                "state": status.channel_1_state.value,
                "voltage": source_voltages[0],
                "current": source_currents[0],
            },
            {
                "channel": 2,
                "supply_mode": status.channel_2_supply_mode.value,
                "state": status.channel_2_state.value,
                "voltage": source_voltages[1],
                "current": source_currents[1],
            },
        ]

        await channel_status_manager.broadcast_json(payload)
        LAST_STATUS = status
        LAST_STATUS_PAYLOAD = payload
        LAST_SOURCE_VOLTAGES = source_voltages
        LAST_SOURCE_CURRENTS = source_currents

    channels = [ps.channel_1]

    for c in channels:
        meas = MeasurementCreate(
            i_device_id=1,
            i_channel_id=c.channel,
            i_measurement_type=1,
            i_value=c.voltage,
            d_datetime=WorkbenchHelper.get_datetime_now_to_nearest_sec(),
        )
        logging_database.insert_measurement(meas)

        meas = MeasurementCreate(
            i_device_id=1,
            i_channel_id=c.channel,
            i_measurement_type=2,
            i_value=c.current,
            d_datetime=WorkbenchHelper.get_datetime_now_to_nearest_sec(),
        )
        logging_database.insert_measurement(meas)


@app.on_event("startup")
@repeat_every(seconds=5)
def insert_fake_power_supply_data() -> None:

    if ps is not None:
        return

    new_measurement: MeasurementCreate = MeasurementCreate(
        i_measurement_type=1,
        i_device_id=1,
        i_channel_id=1,
        d_datetime=WorkbenchHelper.get_datetime_now_to_nearest_sec(),
        i_value=WorkbenchHelper.get_float_with_variation(
            mid_point=5, max_variation=0.25, decimal_places=1
        ),
    )

    logging_database.insert_measurement(new_measurement)

    new_measurement = MeasurementCreate(
        i_measurement_type=2,
        i_device_id=1,
        i_channel_id=1,
        d_datetime=WorkbenchHelper.get_datetime_now_to_nearest_sec(),
        i_value=WorkbenchHelper.get_float_with_variation(
            mid_point=0.100, max_variation=0.050, decimal_places=3
        ),
    )

    logging_database.insert_measurement(new_measurement)


if __name__ == "__main__":
    uvicorn.run(
        # "workbench_web:app", host="localhost", port=5000, reload=True, log_level="debug"
        "workbench_web:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="debug",
    )
