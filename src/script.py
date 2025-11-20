from dataclasses import dataclass
import asyncio
import logging
from typing import Optional, Union, Dict, Any
from enum import Enum
from pymodbus.client import AsyncModbusSerialClient, AsyncModbusTcpClient
from pymodbus import FramerType, ModbusException
import asyncio.exceptions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


class RTUError(Exception): ...
class ASCIIError(Exception): ...
class TCPError(Exception): ...
class DeviceTimeoutError(Exception): ...
class DeviceNoResponseError(Exception): ...
class DeviceInvalidFrameError(Exception): ...
class InternalCancelledError(Exception): ...


class RTUConfig:
    def __init__(self, port="COM1", baudrate=9600, bytesize=8, parity="N",
                 stopbits=1, timeout=3.0, slave_id=1, start_address=0, read_count=2):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.slave_id = slave_id
        self.start_address = start_address
        self.read_count = read_count


class ASCIIConfig:
    def __init__(self, port="COM1", baudrate=9600, bytesize=8, parity="N",
                 stopbits=1, timeout=3.0, slave_id=1, start_address=0, read_count=2):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.slave_id = slave_id
        self.start_address = start_address
        self.read_count = read_count


class TCPConfig:
    def __init__(self, host="127.0.0.1", port=502, timeout=3.0,
                 slave_id=1, start_address=0, read_count=2):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.slave_id = slave_id
        self.start_address = start_address
        self.read_count = read_count


class LogConfiguration:
    def __init__(self, limit=100, since_seconds=3600):
        self.limit = limit
        self.since_seconds = since_seconds


class MQTTConfig:
    def __init__(self, broker="127.0.0.1", port=1883, topic="imod32/log", client_id="imod32-client"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id


GLOBAL_CONFIG: Optional[Union[RTUConfig, ASCIIConfig, TCPConfig]] = None
POLL_INTERVAL_SEC: float = 2.0


def set_config(config: Union[RTUConfig, ASCIIConfig, TCPConfig]):
    """
    Parameters:
        config: RTUConfig | ASCIIConfig | TCPConfig
    Returns:
        None
    """
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = config
    logging.info(f"Configuration updated: {type(config).__name__}")


def set_interval_frequency(ms: int):
    """
    Parameters:
        ms (int): Polling interval in milliseconds.
    Returns:
        None
    """
    global POLL_INTERVAL_SEC
    if ms < 100:
        ms = 100
    POLL_INTERVAL_SEC = ms / 1000
    logging.info(f"Polling interval set to {POLL_INTERVAL_SEC}s")


async def _diagnose_and_raise(e: Exception, protocol: str):
    """
    Parameters:
        e (Exception): caught exception
        protocol (str): 'RTU' | 'ASCII' | 'TCP'
    Returns:
        None
    """
    if isinstance(e, asyncio.TimeoutError):
        raise DeviceTimeoutError(f"{protocol} timeout: Device did not respond")

    if isinstance(e, asyncio.CancelledError):
        raise InternalCancelledError(f"{protocol} async task cancelled")

    if isinstance(e, ModbusException):
        raise DeviceInvalidFrameError(f"{protocol} invalid or unexpected frame: {e}")

    raise Exception(f"{protocol} unknown error: {e}")


async def _pull_data_rtu(config: RTUConfig):
    """
    Parameters:
        config (RTUConfig)
    Returns:
        None
    """
    client = AsyncModbusSerialClient(
        port=config.port,
        framer=FramerType.RTU,
        baudrate=config.baudrate,
        bytesize=config.bytesize,
        parity=config.parity,
        stopbits=config.stopbits,
        timeout=config.timeout
    )

    try:
        if not await client.connect():
            raise RTUError(f"Cannot open RTU port {config.port}")

        logging.info(f"RTU connected on {config.port}")

        while True:
            try:
                result = await client.read_holding_registers(
                    address=config.start_address,
                    count=config.read_count,
                    slave=config.slave_id
                )
                if result.isError():
                    raise DeviceInvalidFrameError(f"RTU error frame: {result}")

                logging.info(f"RTU registers: {result.registers}")
                await asyncio.sleep(POLL_INTERVAL_SEC)

            except Exception as e:
                await _diagnose_and_raise(e, "RTU")

    finally:
        client.close()
        logging.info("RTU closed")


async def _pull_data_ascii(config: ASCIIConfig):
    """
    Parameters:
        config (ASCIIConfig)
    Returns:
        None
    """
    client = AsyncModbusSerialClient(
        port=config.port,
        framer=FramerType.ASCII,
        baudrate=config.baudrate,
        bytesize=config.bytesize,
        parity=config.parity,
        stopbits=config.stopbits,
        timeout=config.timeout
    )

    try:
        if not await client.connect():
            raise ASCIIError(f"Cannot open ASCII port {config.port}")

        logging.info(f"ASCII connected on {config.port}")

        while True:
            try:
                result = await client.read_holding_registers(
                    address=config.start_address,
                    count=config.read_count,
                    slave=config.slave_id
                )
                if result.isError():
                    raise DeviceInvalidFrameError(f"ASCII error frame: {result}")

                logging.info(f"ASCII registers: {result.registers}")
                await asyncio.sleep(POLL_INTERVAL_SEC)

            except Exception as e:
                await _diagnose_and_raise(e, "ASCII")

    finally:
        client.close()
        logging.info("ASCII closed")


async def _pull_data_tcp(config: TCPConfig):
    """
    Parameters:
        config (TCPConfig)
    Returns:
        None
    """
    client = AsyncModbusTcpClient(config.host, config.port, timeout=config.timeout)

    try:
        if not await client.connect():
            raise TCPError(f"Cannot connect TCP {config.host}:{config.port}")

        logging.info(f"TCP connected to {config.host}:{config.port}")

        while True:
            try:
                result = await client.read_holding_registers(
                    address=config.start_address,
                    count=config.read_count,
                    slave=config.slave_id
                )

                if result.isError():
                    raise DeviceInvalidFrameError(f"TCP error frame: {result}")

                logging.info(f"TCP registers: {result.registers}")
                await asyncio.sleep(POLL_INTERVAL_SEC)

            except Exception as e:
                await _diagnose_and_raise(e, "TCP")

    finally:
        client.close()
        logging.info("TCP closed")


async def pull_data():
    """
    Parameters:
        None
    Returns:
        None
    """
    config = GLOBAL_CONFIG

    if isinstance(config, RTUConfig):
        await _pull_data_rtu(config)

    elif isinstance(config, ASCIIConfig):
        await _pull_data_ascii(config)

    elif isinstance(config, TCPConfig):
        await _pull_data_tcp(config)

    else:
        raise Exception(f"Unsupported config type {type(config).__name__}")
    
async def push_data_rtu_over_tcp(config: TCPConfig, value: int):
    """
    Parameters:
        config (TCPConfig): RTU-over-TCP gateway connection.
        value (int): Value to write.
    Returns:
        None
    """
    client = AsyncModbusTcpClient(
        host=config.host,
        port=config.port,
        timeout=config.timeout
    )

    try:
        if not await client.connect():
            raise TCPError(f"Cannot connect RTU-over-TCP {config.host}:{config.port}")

        result = await client.write_register(
            address=config.start_address,
            value=value,
            slave=config.slave_id
        )

        if result.isError():
            raise DeviceInvalidFrameError(f"RTU-over-TCP write failed: {result}")

        logging.info(f"RTU-over-TCP write OK: {value}")

    except Exception as e:
        await _diagnose_and_raise(e, "RTU-over-TCP")

    finally:
        client.close()
        logging.info("RTU-over-TCP closed")

async def push_data_ascii(config: ASCIIConfig, value: int):
    """
    Parameters:
        config (ASCIIConfig): ASCII serial configuration.
        value (int): Value to write.
    Returns:
        None
    """
    client = AsyncModbusSerialClient(
        port=config.port,
        framer=FramerType.ASCII,
        baudrate=config.baudrate,
        bytesize=config.bytesize,
        parity=config.parity,
        stopbits=config.stopbits,
        timeout=config.timeout
    )

    try:
        if not await client.connect():
            raise ASCIIError(f"Cannot open ASCII port {config.port}")

        result = await client.write_register(
            address=config.start_address,
            value=value,
            slave=config.slave_id
        )

        if result.isError():
            raise DeviceInvalidFrameError(f"ASCII write failed: {result}")

        logging.info(f"ASCII write OK: {value}")

    except Exception as e:
        await _diagnose_and_raise(e, "ASCII")

    finally:
        client.close()
        logging.info("ASCII closed")


import threading

POLLING_THREAD = None

def apply_config_from_api(payload: dict):
    """
    Parameters:
        payload (dict): REST config payload.
    Returns:
        None
    """
    conn_type = payload.get("type")

    if conn_type == "RTU":
        cfg = RTUConfig(
            port=payload["port"],
            baudrate=payload["baudrate"],
            parity=payload["parity"],
            slave_id=payload["slave_id"],
            start_address=payload["start_address"],
            read_count=payload["read_count"]
        )
        set_config(cfg)

    elif conn_type == "ASCII":
        cfg = ASCIIConfig(
            port=payload["port"],
            baudrate=payload["baudrate"],
            parity=payload["parity"],
            slave_id=payload["slave_id"],
            start_address=payload["start_address"],
            read_count=payload["read_count"]
        )
        set_config(cfg)

    elif conn_type == "TCP":
        cfg = TCPConfig(
            host=payload["host"],
            port=payload["port"],
            slave_id=payload["slave_id"],
            start_address=payload["start_address"],
            read_count=payload["read_count"]
        )
        set_config(cfg)

    if "interval_ms" in payload:
        set_interval_frequency(payload["interval_ms"])

async def poll_and_collect(interval_ms: int, length_sec: int):
    """
    Parameters:
        interval_ms (int): Polling interval.
        length_sec (int): Total polling duration.
    Returns:
        list: Collected readings.
    """
    global GLOBAL_CONFIG
    results = []

    # Set interval
    set_interval_frequency(interval_ms)

    # Convert to seconds
    end_time = asyncio.get_event_loop().time() + length_sec

    while asyncio.get_event_loop().time() < end_time:

        try:
            if isinstance(GLOBAL_CONFIG, RTUConfig):
                client = AsyncModbusSerialClient(
                    port=GLOBAL_CONFIG.port,
                    framer=FramerType.RTU,
                    baudrate=GLOBAL_CONFIG.baudrate,
                    bytesize=GLOBAL_CONFIG.bytesize,
                    parity=GLOBAL_CONFIG.parity,
                    stopbits=GLOBAL_CONFIG.stopbits,
                    timeout=GLOBAL_CONFIG.timeout
                )
            elif isinstance(GLOBAL_CONFIG, ASCIIConfig):
                client = AsyncModbusSerialClient(
                    port=GLOBAL_CONFIG.port,
                    framer=FramerType.ASCII,
                    baudrate=GLOBAL_CONFIG.baudrate,
                    bytesize=GLOBAL_CONFIG.bytesize,
                    parity=GLOBAL_CONFIG.parity,
                    stopbits=GLOBAL_CONFIG.stopbits,
                    timeout=GLOBAL_CONFIG.timeout
                )
            elif isinstance(GLOBAL_CONFIG, TCPConfig):
                client = AsyncModbusTcpClient(
                    host=GLOBAL_CONFIG.host,
                    port=GLOBAL_CONFIG.port,
                    timeout=GLOBAL_CONFIG.timeout
                )
            else:
                raise Exception("Unsupported config")

            if not await client.connect():
                raise DeviceNoResponseError("Device not reachable")

            resp = await client.read_holding_registers(
                address=GLOBAL_CONFIG.start_address,
                count=GLOBAL_CONFIG.read_count,
                slave=GLOBAL_CONFIG.slave_id
            )

            if resp.isError():
                raise DeviceInvalidFrameError("Invalid Modbus frame")

            moisture = resp.registers[0] / 10.0
            temperature = resp.registers[1] / 10.0

            results.append({
                resp
            })

        except Exception as e:
            results.append({"error": str(e)})

        finally:
            client.close()

        await asyncio.sleep(POLL_INTERVAL_SEC)

    return results



# config = RTUConfig(
#     port="COM4",
#     baudrate=4800,
#     slave_id=1,
#     start_address=0,
#     read_count=2
# )

# set_config(config)
# set_interval_frequency(1500) 
# asyncio.run(pull_data())
