import asyncio
import json
import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from home_workbench.spd3303c import SPD3303C


def get_full_path_from_cwd(path):
    root = os.path.dirname(os.path.realpath(__file__))
    return f"{root}\\{path}"


app = FastAPI()
templates_path = get_full_path_from_cwd("templates")
print(templates_path)
templates = Jinja2Templates(directory=templates_path)
ps = SPD3303C()


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
