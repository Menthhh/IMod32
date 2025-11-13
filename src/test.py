from main import HardwareDataFlow, SerialConfig, LogConfiguration, MQTTConfig

def run_tests():
    """
    Runs a series of tests to demonstrate the functionality of the 
    HardwareDataFlow class methods based on the data flow structure.
    """
    print("--- Running Hardware Data Flow Demonstration ---")
    
    flow = HardwareDataFlow()

    # --- 1. Pull Data Tests ---
    print("\n--- 1. Pull Data ---")
    rtu_data = flow.pull_data(protocol='RTU')
    ascii_data = flow.pull_data(protocol='ASCII')
    print(f"Result (RTU): {rtu_data}")
    print(f"Result (ASCII): {ascii_data}")

    # --- 2. Set Interval Test ---
    print("\n--- 2. Set Interval ---")
    success_interval = flow.set_interval_frequency(ms=500)
    failure_interval = flow.set_interval_frequency(ms=10)
    print(f"Set 500ms successful: {success_interval}")
    print(f"Set 10ms successful: {failure_interval}")

    # --- 3. Calculate Tests ---
    print("\n--- 3. Calculate ---")
    
    # 3.1 Calculate for Record
    record_output = flow.calculate_for_record(formation='Telemetry', block_code='Block_A')
    print(f"Record Calculation Result: {record_output}")

    # 3.2 Calculate for Alarm
    alarm_low = flow.calculate_for_alarm(formation='Sensor', block_code='Block_Temp_LOW')
    alarm_high = flow.calculate_for_alarm(formation='Sensor', block_code='Block_Pressure_HIGH')
    print(f"Alarm Check (LOW): {alarm_low} (Expected: False)")
    print(f"Alarm Check (HIGH): {alarm_high} (Expected: True)")


    # --- 4. Serial Configuration Test ---
    print("\n--- 4. Serial Configuration ---")
    serial_config = SerialConfig(port='/dev/ttyUSB0', baud_rate=9600, parity='E', data_bits=7)
    config_result = flow.set_serial_configuration(serial_config)
    print(f"Serial Configuration Applied: {config_result}")

    # --- 5. Push Data Tests ---
    print("\n--- 5. Push Data ---")
    push_rtu_data = "PROCESSED_DATA_123"
    push_ascii_data = "JSON_DATA_STREAM"

    push_rtu_result = flow.push_data(protocol='RTU', data=push_rtu_data)
    push_ascii_result = flow.push_data(protocol='ASCII', data=push_ascii_data)

    print(f"RTU Push Result: {push_rtu_result}")
    print(f"ASCII Push Result: {push_ascii_result}")

    # --- 6. API Test ---
    print("\n--- 6. API ---")
    log_config = LogConfiguration(
        start_time='2023-10-01T00:00:00Z', 
        end_time='2023-10-02T00:00:00Z', 
        log_type='Maintenance'
    )
    rest_logs = flow.pull_log_by_rest(device_id='HW-PLC-001', log_config=log_config)
    print(f"REST Log Count Retrieved: {len(rest_logs)}")
    print(f"Sample Log: {rest_logs[0]}")

    # --- 7. MQTT Connection Test ---
    print("\n--- 7. MQTT Connection ---")
    mqtt_config = MQTTConfig(
        broker='mqtt.cloudservice.com', 
        topic='devices/HW-PLC-001/logs',
        qos=1
    )
    mqtt_status = flow.pull_log_by_mqtt(mqtt_config)
    print(f"MQTT Status: {mqtt_status}")
    print("\n--- Demonstration Complete ---")

if __name__ == '__main__':
    run_tests()