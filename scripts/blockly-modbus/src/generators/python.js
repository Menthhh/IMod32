import { pythonGenerator } from 'blockly/python';

export const forBlock = Object.create(null);

forBlock['RTU_config'] = function (block, generator) {
  const Order = generator.ORDER_ATOMIC || 0;

  const port = generator.valueToCode(block, 'PORT', Order) || '"COM4"';
  const baudrate = block.getFieldValue('BAUDRATE');
  const bytesize = generator.valueToCode(block, 'BYTESIZE', Order) || '8';
  const parity = block.getFieldValue('PARITY');
  const stopbits = generator.valueToCode(block, 'STOPBITS', Order) || '1';
  const timeout = generator.valueToCode(block, 'TIMEOUT', Order) || '3.0';
  const slave_id = generator.valueToCode(block, 'SLAVE_ID', Order) || '1';
  const start_address = generator.valueToCode(block, 'START_ADDRESS', Order) || '0';
  const count = generator.valueToCode(block, 'COUNT', Order) || '3';
  const function_code = block.getFieldValue('FUNCTION_CODE');

  const code = `connection_type.RTUConfig(
    port=${port},
    baudrate=${baudrate},
    bytesize=${bytesize},
    parity="${parity}",
    stopbits=${stopbits},
    timeout=${timeout},
    slave_id=${slave_id},
    start_address=${start_address},
    count=${count},
    function_code=${function_code}
)`;
  return [code, Order];
};

forBlock['ASCII_config'] = function (block, generator) {
  const Order = generator.ORDER_ATOMIC || 0;

  const port = generator.valueToCode(block, 'PORT', Order) || '"COM4"';
  const baudrate = block.getFieldValue('BAUDRATE');
  const bytesize = generator.valueToCode(block, 'BYTESIZE', Order) || '8';
  const parity = block.getFieldValue('PARITY');
  const stopbits = generator.valueToCode(block, 'STOPBITS', Order) || '1';
  const timeout = generator.valueToCode(block, 'TIMEOUT', Order) || '3.0';
  const slave_id = generator.valueToCode(block, 'SLAVE_ID', Order) || '1';
  const start_address = generator.valueToCode(block, 'START_ADDRESS', Order) || '0';
  const count = generator.valueToCode(block, 'COUNT', Order) || '3';
  const function_code = block.getFieldValue('FUNCTION_CODE');

  const code = `connection_type.ASCIIConfig(
    port=${port},
    baudrate=${baudrate},
    bytesize=${bytesize},
    parity="${parity}",
    stopbits=${stopbits},
    timeout=${timeout},
    slave_id=${slave_id},
    start_address=${start_address},
    count=${count},
    function_code=${function_code}
)`;
  return [code, Order];
};

forBlock['TCP_config'] = function (block, generator) {
  const Order = generator.ORDER_ATOMIC || 0;

  const host = generator.valueToCode(block, 'HOST', Order) || '"127.0.0.1"';
  const port = generator.valueToCode(block, 'PORT', Order) || '502';
  const timeout = generator.valueToCode(block, 'TIMEOUT', Order) || '3.0';
  const slave_id = generator.valueToCode(block, 'SLAVE_ID', Order) || '1';
  const start_address = generator.valueToCode(block, 'START_ADDRESS', Order) || '0';
  const count = generator.valueToCode(block, 'COUNT', Order) || '2';
  const function_code = block.getFieldValue('FUNCTION_CODE');

  const code = `connection_type.TCPConfig(
    host=${host},
    port=${port},
    timeout=${timeout},
    slave_id=${slave_id},
    start_address=${start_address},
    count=${count},
    function_code=${function_code}
)`;
  return [code, Order];
};

forBlock['modbus_pull_data'] = function (block, generator) {
  const Order = generator.ORDER_AWAIT || 3;
  const config = generator.valueToCode(block, 'CONFIG', generator.ORDER_NONE) || 'None';

  // Inject imports (idempotent)
  generator.definitions_['import_modbus_types'] = 'from connection_type import RTUConfig, ASCIIConfig, TCPConfig';
  generator.definitions_['import_poll'] = 'from poll import pull_data_async, set_interval_frequency';
  generator.definitions_['import_asyncio'] = 'import asyncio';

  const code = `await pull_data_async(${config})`;
  return [code, Order];
};

forBlock['set_modbus_interval'] = function (block, generator) {
  const interval_ms = generator.valueToCode(block, 'INTERVAL_MS', generator.ORDER_NONE) || '1000';

  // Inject imports (idempotent)
  generator.definitions_['import_poll'] = 'from poll import pull_data_async, set_interval_frequency';

  const code = `set_interval_frequency(${interval_ms})\n`;
  return code;
};

forBlock['modbus_get_field'] = function (block, generator) {
  const Order = generator.ORDER_MEMBER || 2;
  const field = block.getFieldValue('FIELD');
  const data = generator.valueToCode(block, 'DATA', generator.ORDER_MEMBER) || '{}';

  const code = `${data}.get('${field}')`;
  return [code, Order];
};

forBlock['modbus_task_definition'] = function (block, generator) {
  const task_id = block.getFieldValue('TASK_ID');
  const interval = block.getFieldValue('INTERVAL');
  const statements_do = generator.statementToCode(block, 'DO');

  // Register this task ID to be run in main
  if (!generator.modbus_tasks_) {
    generator.modbus_tasks_ = [];
  }
  const funcName = `task_${task_id}_loop`;
  generator.modbus_tasks_.push(funcName);

  // Inject imports
  generator.definitions_['import_asyncio'] = 'import asyncio';
  generator.definitions_['import_poll'] = 'from poll import pull_data_async, set_interval_frequency';

  const code = `
async def ${funcName}():
    while True:
        set_interval_frequency(${interval} * 1000)
${statements_do}
        await asyncio.sleep(${interval})
`;
  return code;
};

forBlock['modbus_get_register'] = function (block, generator) {
  const Order = generator.ORDER_MEMBER || 2;
  const index = generator.valueToCode(block, 'INDEX', generator.ORDER_NONE) || '0';
  const data = generator.valueToCode(block, 'DATA', generator.ORDER_MEMBER) || '{}';

  const code = `${data}.get('registers')[${index}]`;
  return [code, Order];
};

forBlock['modbus_get_limiter'] = function (block, generator) {
  const Order = generator.ORDER_FUNCTION_CALL || 1;
  const name = block.getFieldValue('LIMITER_NAME');
  const code = `get_limiter('${name}')`;
  return [code, Order];
};

forBlock['modbus_dcp_update'] = function (block, generator) {
  const name = block.getFieldValue('NAME');
  const value = generator.valueToCode(block, 'VALUE', generator.ORDER_NONE) || '0';

  const code = `dcp_update('${name}', ${value})\n`;
  return code;
};

forBlock['modbus_alarm_evaluator'] = function (block, generator) {
  const Order = generator.ORDER_CONDITIONAL || 6;
  const val = generator.valueToCode(block, 'VAL', generator.ORDER_RELATIONAL) || '0';
  const lv1 = generator.valueToCode(block, 'LV1', generator.ORDER_RELATIONAL) || '0';
  const lv2 = generator.valueToCode(block, 'LV2', generator.ORDER_RELATIONAL) || '0';
  const lv3 = generator.valueToCode(block, 'LV3', generator.ORDER_RELATIONAL) || '0';

  const code = `("LV1" if ${val} >= ${lv1} and ${val} < ${lv2} else "LV2" if ${val} >= ${lv2} and ${val} < ${lv3} else "LV3" if ${val} >= ${lv3} else "LV0")`;
  return [code, Order];
};

forBlock['modbus_log'] = function (block, generator) {
  const msg = generator.valueToCode(block, 'MSG', generator.ORDER_NONE) || '""';
  const code = `print(${msg})\n`;
  return code;
};

/**
 * Override the finish method to append the main runner.
 */
const originalFinish = pythonGenerator.finish;
pythonGenerator.finish = function (code) {
  // Call the original finish to handle imports and definitions
  let completedCode = originalFinish.call(this, code);

  // If we have defined tasks, generate the main runner
  if (this.modbus_tasks_ && this.modbus_tasks_.length > 0) {
    const taskCalls = this.modbus_tasks_.map(t => `${t}()`).join(', ');
    const mainRunner = `
async def main():
    await asyncio.gather(${taskCalls})

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
`;
    completedCode += mainRunner;
  }

  // Clean up for next run
  this.modbus_tasks_ = [];

  return completedCode;
};