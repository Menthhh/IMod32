from poll import pull_data, set_interval_frequency
import connection_type

cfg = connection_type.RTUConfig(
    port="COM4",
    baudrate=4800,
    start_address=0,
    count=3,
    function_code=4
)
set_interval_frequency(1500)
# [Byte Count] [Register1(2 bytes)] [Register2(2 bytes)] ... [RegN]
while True:
    result = pull_data(cfg)
    print(result)
    # Calculate alarm or any formula below


