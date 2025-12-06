import * as Blockly from 'blockly/core';

const RTU_config_json = {
  type: 'RTU_config',
  message0: 'MODBUS RTU Config Port: %1 Baudrate: %2 Addr: %3 Count: %4 FC: %5 ID: %6',
  args0: [
    { type: 'field_input', name: 'PORT', text: 'COM4' },
    { type: 'field_number', name: 'BAUDRATE', value: 4800, min: 1 },
    { type: 'field_number', name: 'START_ADDRESS', value: 0, min: 0 },
    { type: 'field_number', name: 'COUNT', value: 3, min: 1 },
    {
      type: 'field_dropdown',
      name: 'FUNCTION_CODE',
      options: [
        ['Input Registers (4)', '4'],
        ['Holding Registers (3)', '3'],
        ['Coils (1)', '1'],
        ['Discrete Inputs (2)', '2']
      ]
    },
    { type: 'field_number', name: 'SLAVE_ID', value: 1, min: 1, max: 247 }
  ],
  output: 'Config', 
  colour: 160,
  tooltip: 'Configures a Modbus RTU serial connection.',
  helpUrl: '',
};

const TCP_config_json = {
  type: 'TCP_config',
  message0: 'MODBUS TCP Config Host: %1 Port: %2 Addr: %3 Count: %4 FC: %5',
  args0: [
    { type: 'field_input', name: 'HOST', text: '127.0.0.1' },
    { type: 'field_number', name: 'PORT', value: 502 },
    { type: 'field_number', name: 'START_ADDRESS', value: 0, min: 0 },
    { type: 'field_number', name: 'COUNT', value: 2, min: 1 },
    {
      type: 'field_dropdown',
      name: 'FUNCTION_CODE',
      options: [
        ['Holding Registers (3)', '3'],
        ['Input Registers (4)', '4']
      ]
    }
  ],
  output: 'Config',
  colour: 160,
  tooltip: 'Configures a Modbus TCP/IP connection.',
  helpUrl: '',
};

// export const blocks = Blockly.common.createBlockDefinitionsFromJsonArray([
//   RTU_config_json,
//   TCP_config_json
// ]);
Blockly.defineBlocksWithJsonArray([
  RTU_config_json,
  TCP_config_json
]);
