from dataclasses import dataclass
from typing import Optional
import asyncio
import logging
from pymodbus.client import AsyncModbusSerialClient
from pymodbus import FramerType, ModbusException

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

@dataclass
class ModbusRTUConfig:
    baudrate: int = 9600
    bytesize: int = 8
    parity: str = 'N'
    stopbits: int = 1
    timeout: float = 3.0
    slave_id: int = 1
    start_address: int = 0
    read_count: int = 2
    framer_type: FramerType = FramerType.RTU

class Modbus32:
    def __init__(self):
        self.client: Optional[AsyncModbusSerialClient] = None

    async def pull_data(self, port: str, config: ModbusRTUConfig):
        logging.info(f"Connecting to {port} at {config.baudrate} using {config.framer_type.name}...")
        self.client = AsyncModbusSerialClient(
            port=port,
            framer=config.framer_type,
            baudrate=config.baudrate,
            bytesize=config.bytesize,
            parity=config.parity,
            stopbits=config.stopbits,
            timeout=config.timeout,
        )
        try:
            await self.client.connect()
        except Exception as e:
            logging.error(f"Error connecting to port {port}: {e}")
            return
        if not self.client.connected:
            logging.error(f"Failed to establish connection to {port}.")
            return
        logging.info("Connection successful. Reading registers...")
        try:
            while True:
                result = await self.client.read_holding_registers(
                    address=config.start_address,
                    count=config.read_count,
                    slave=config.slave_id
                )
                if result.isError():
                    logging.warning(f"Modbus read failed: {result}")
                    return
                raw_moisture = result.registers[0]
                raw_temp = result.registers[1]
                moisture = raw_moisture / 10.0
                temperature = raw_temp / 10.0
                logging.info(f"Read OK | Moisture: {moisture:.1f}% | Temp: {temperature:.1f}°C")
                await asyncio.sleep(2)
        except ModbusException as exc:
            logging.error(f"Modbus Library Exception: {exc}")
        except Exception as e:
            logging.error(f"Unexpected Error: {e}")
        finally:
            if self.client and self.client.connected:
                try:
                    await self.client.close()
                except Exception as e:
                    logging.warning(f"Error closing connection: {e}")
            logging.info("Client connection closed.")

    def run(self, port: str, config: ModbusRTUConfig):
        logging.info("Starting Modbus32 asynchronous operation...")
        asyncio.run(self.pull_data(port, config))

if __name__ == "__main__":
    settings = ModbusRTUConfig(
        baudrate=4800,
        parity='N',
        slave_id=1,
        start_address=0,
        read_count=2,
        framer_type=FramerType.RTU
    )
    modbus_device = Modbus32()
    modbus_device.run(port="COM4", config=settings)
