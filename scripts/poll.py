import asyncio
import logging
from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus import FramerType
from connection_type import RTUConfig, ASCIIConfig, TCPConfig

logging.basicConfig(level=logging.INFO)

class DeviceTimeoutError(Exception): ...


POLL_INTERVAL_SEC = 1.0

def set_interval_frequency(ms: int):
    global POLL_INTERVAL_SEC
    if ms < 100:
        ms = 100
    POLL_INTERVAL_SEC = ms / 1000

async def _build_client(config):
    if isinstance(config, RTUConfig):
        return AsyncModbusSerialClient(
            port=config.port,
            framer=FramerType.RTU,
            baudrate=config.baudrate,
            bytesize=config.bytesize,
            parity=config.parity,
            stopbits=config.stopbits,
            timeout=config.timeout
        )
    if isinstance(config, ASCIIConfig):
        return AsyncModbusSerialClient(
            port=config.port,
            framer=FramerType.ASCII,
            baudrate=config.baudrate,
            bytesize=config.bytesize,
            parity=config.parity,
            stopbits=config.stopbits,
            timeout=config.timeout
        )
    if isinstance(config, TCPConfig):
        return AsyncModbusTcpClient(
            host=config.host,
            port=config.port,
            timeout=config.timeout
        )
    raise Exception("Unsupported config")

async def pull_data_async(config):
    await asyncio.sleep(POLL_INTERVAL_SEC)
    client = await _build_client(config)

    try:
        if not await client.connect():
            raise DeviceTimeoutError("Device not reachable")

        if config.function_code == 1:
            resp = await client.read_coils(
                address=config.start_address,
                count=config.count,
                slave=config.slave_id
            )
        elif config.function_code == 2:
            resp = await client.read_discrete_inputs(
                address=config.start_address,
                count=config.count,
                slave=config.slave_id
            )
        elif config.function_code == 3:
            resp = await client.read_holding_registers(
                address=config.start_address,
                count=config.count,
                slave=config.slave_id
            )
        elif config.function_code == 4:
            resp = await client.read_input_registers(
                address=config.start_address,
                count=config.count,
                slave=config.slave_id
            )
        else:
            raise Exception("Unsupported function code")
        return {
            "raw": resp.encode().hex(),
            "registers": getattr(resp, "registers", None),
            # "objects": resp
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        client.close()

def pull_data(config):
    return asyncio.run(pull_data_async(config))
