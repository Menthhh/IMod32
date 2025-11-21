class RTUConfig:
    def __init__(self, port="COM1", baudrate=9600, bytesize=8, parity="N",
                 stopbits=1, timeout=3.0, slave_id=1, start_address=0,
                 count=2, function_code=3):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.slave_id = slave_id
        self.start_address = start_address
        self.count = count
        self.function_code = function_code

class ASCIIConfig:
    def __init__(self, port="COM1", baudrate=9600, bytesize=8, parity="N",
                 stopbits=1, timeout=3.0, slave_id=1, start_address=0,
                 count=2, function_code=3):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.slave_id = slave_id
        self.start_address = start_address
        self.count = count
        self.function_code = function_code

class TCPConfig:
    def __init__(self, host="127.0.0.1", port=502, timeout=3.0,
                 slave_id=1, start_address=0, count=2, function_code=3):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.slave_id = slave_id
        self.start_address = start_address
        self.count = count
        self.function_code = function_code