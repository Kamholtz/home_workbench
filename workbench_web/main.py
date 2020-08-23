import json
import asyncio
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates
import os

def get_full_path_from_cwd(path):
    root = os.path.dirname(os.path.realpath(__file__))
    return f'{root}\{path}'

app = FastAPI()
templates_path = get_full_path_from_cwd("templates")
print(templates_path)
templates = Jinja2Templates(directory=templates_path)

with open(get_full_path_from_cwd('measurements.json'), 'r') as file:
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
        await websocket.send_json(payload)