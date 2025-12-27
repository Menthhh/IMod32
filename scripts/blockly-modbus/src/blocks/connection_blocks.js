import * as Blockly from 'blockly/core';

const RTU_config_json = {
  type: 'RTU_config',
  message0: 'MODBUS RTU Config %1 Port: %2 Baudrate: %3 Bytesize: %4 Parity: %5 Stopbits: %6 Timeout: %7 Slave ID: %8 Addr: %9 Count: %10 FC: %11',
  args0: [
    { type: 'input_dummy' },
    { type: 'input_value', name: 'PORT', check: 'String' },
    {
      type: 'field_dropdown',
      name: 'BAUDRATE',
      options: [
        ['9600', '9600'],
        ['19200', '19200'],
        ['115200', '115200']
      ]
    },
    { type: 'input_value', name: 'BYTESIZE', check: 'Number' },
    {
      type: 'field_dropdown',
      name: 'PARITY',
      options: [
        ['None (N)', 'N'],
        ['Even (E)', 'E'],
        ['Odd (O)', 'O']
      ]
    },
    { type: 'input_value', name: 'STOPBITS', check: 'Number' },
    { type: 'input_value', name: 'TIMEOUT', check: 'Number' },
    { type: 'input_value', name: 'SLAVE_ID', check: 'Number' },
    { type: 'input_value', name: 'START_ADDRESS', check: 'Number' },
    { type: 'input_value', name: 'COUNT', check: 'Number' },
    {
      type: 'field_dropdown',
      name: 'FUNCTION_CODE',
      options: [
        ['Coils (1)', '1'],
        ['Discrete Inputs (2)', '2'],
        ['Holding Registers (3)', '3'],
        ['Input Registers (4)', '4']
      ]
    }
  ],
  output: 'ModbusConfig',
  colour: 160,
  tooltip: 'Configures a Modbus RTU serial connection.',
  helpUrl: '',
};

const ASCII_config_json = {
  type: 'ASCII_config',
  message0: 'MODBUS ASCII Config %1 Port: %2 Baudrate: %3 Bytesize: %4 Parity: %5 Stopbits: %6 Timeout: %7 Slave ID: %8 Addr: %9 Count: %10 FC: %11',
  args0: [
    { type: 'input_dummy' },
    { type: 'input_value', name: 'PORT', check: 'String' },
    {
      type: 'field_dropdown',
      name: 'BAUDRATE',
      options: [
        ['9600', '9600'],
        ['19200', '19200'],
        ['115200', '115200']
      ]
    },
    { type: 'input_value', name: 'BYTESIZE', check: 'Number' },
    {
      type: 'field_dropdown',
      name: 'PARITY',
      options: [
        ['None (N)', 'N'],
        ['Even (E)', 'E'],
        ['Odd (O)', 'O']
      ]
    },
    { type: 'input_value', name: 'STOPBITS', check: 'Number' },
    { type: 'input_value', name: 'TIMEOUT', check: 'Number' },
    { type: 'input_value', name: 'SLAVE_ID', check: 'Number' },
    { type: 'input_value', name: 'START_ADDRESS', check: 'Number' },
    { type: 'input_value', name: 'COUNT', check: 'Number' },
    {
      type: 'field_dropdown',
      name: 'FUNCTION_CODE',
      options: [
        ['Coils (1)', '1'],
        ['Discrete Inputs (2)', '2'],
        ['Holding Registers (3)', '3'],
        ['Input Registers (4)', '4']
      ]
    }
  ],
  output: 'ModbusConfig',
  colour: 160,
  tooltip: 'Configures a Modbus ASCII serial connection.',
  helpUrl: '',
};

const TCP_config_json = {
  type: 'TCP_config',
  message0: 'MODBUS TCP Config %1 Host: %2 Port: %3 Timeout: %4 Slave ID: %5 Addr: %6 Count: %7 FC: %8',
  args0: [
    { type: 'input_dummy' },
    { type: 'input_value', name: 'HOST', check: 'String' },
    { type: 'input_value', name: 'PORT', check: 'Number' },
    { type: 'input_value', name: 'TIMEOUT', check: 'Number' },
    { type: 'input_value', name: 'SLAVE_ID', check: 'Number' },
    { type: 'input_value', name: 'START_ADDRESS', check: 'Number' },
    { type: 'input_value', name: 'COUNT', check: 'Number' },
    {
      type: 'field_dropdown',
      name: 'FUNCTION_CODE',
      options: [
        ['Coils (1)', '1'],
        ['Discrete Inputs (2)', '2'],
        ['Holding Registers (3)', '3'],
        ['Input Registers (4)', '4']
      ]
    }
  ],
  output: 'ModbusConfig',
  colour: 160,
  tooltip: 'Configures a Modbus TCP/IP connection.',
  helpUrl: '',
};

Blockly.defineBlocksWithJsonArray([
  RTU_config_json,
  ASCII_config_json,
  TCP_config_json
]);
