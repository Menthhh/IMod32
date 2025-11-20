from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os
import asyncio
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import script

app = FastAPI()

class PullRequest(BaseModel):
    type: str
    port: str = None
    host: str = None
    baudrate: int = 9600
    parity: str = "N"
    slave_id: int = 1
    start_address: int = 0
    read_count: int = 2
    interval_ms: int = 1000
    length_sec: int = 5


@app.post("/pull")
async def pull_once(req: PullRequest):
    script.apply_config_from_api(req.dict())

    data = await script.poll_and_collect(
        interval_ms=req.interval_ms,
        length_sec=req.length_sec
    )

    return {
        "records": data,
        # Readable time
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
