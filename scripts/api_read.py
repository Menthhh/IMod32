import logging
from typing import Optional, Union
from connection_type import RTUConfig, ASCIIConfig, TCPConfig

logging.basicConfig(level=logging.INFO)

GLOBAL_CONFIG: Optional[Union[RTUConfig, ASCIIConfig, TCPConfig]] = None


def set_config(config):
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = config
    logging.info(f"Configuration set → {type(config).__name__}")


def apply_config_from_api(payload: dict):
    conn_type = payload.get("type")
    function_code = payload.get("function_code", 3)
    count = payload.get("count", 1)

    if conn_type == "RTU":
        cfg = RTUConfig(
            port=payload["port"],
            baudrate=payload["baudrate"],
            parity=payload["parity"],
            slave_id=payload["slave_id"],
            start_address=payload["start_address"],
            count=count,
            function_code=function_code
        )
        set_config(cfg)

    elif conn_type == "ASCII":
        cfg = ASCIIConfig(
            port=payload["port"],
            baudrate=payload["baudrate"],
            parity=payload["parity"],
            slave_id=payload["slave_id"],
            start_address=payload["start_address"],
            count=count,
            function_code=function_code
        )
        set_config(cfg)

    elif conn_type == "TCP":
        cfg = TCPConfig(
            host=payload["host"],
            port=payload["port"],
            slave_id=payload["slave_id"],
            start_address=payload["start_address"],
            count=count,
            function_code=function_code
        )
        set_config(cfg)

    else:
        raise ValueError("Invalid connection type")

