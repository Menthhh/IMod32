from pymodbus.client import AsyncModbusSerialClient
import asyncio

async def async_rtu_example():
    """Async RTU client example."""
    client = AsyncModbusSerialClient(
        port='COM4',
        baudrate=4800,
        timeout=1
    )
    
    await client.connect()
    
    # Read from multiple slaves
    while True:
        result = await client.read_holding_registers(0, count=2, slave=1)
        if not result.isError():
            print(f"Slave 1: {result.registers}")
    
    client.close()

asyncio.run(async_rtu_example())