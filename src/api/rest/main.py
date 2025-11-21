# api/rest/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
import time
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import api_read
from poll import pull_data

app = FastAPI()

class PullRequest(BaseModel):
    type: str
    port: str | None = None
    host: str | None = None
    baudrate: int = 9600
    parity: str = "N"
    slave_id: int = 1
    start_address: int = 0
    count: int = 2
    function_code: int = 4
    interval_ms: int = 1000   


@app.post("/pull")
async def pull_once(req: PullRequest):
    api_read.apply_config_from_api(req.dict())
    result = await asyncio.to_thread(pull_data, api_read.GLOBAL_CONFIG)
    return {
        "record": result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
