import * as Blockly from 'blockly/core';

Blockly.defineBlocksWithJsonArray([
  {
    type: 'python_print',
    message0: 'print %1',
    args0: [{ type: 'input_value', name: 'VALUE' }],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: 'Print a value to the output',
    helpUrl: '',
  },
  {
    type: 'python_input',
    message0: 'input( %1 )',
    args0: [{ type: 'input_value', name: 'PROMPT', check: 'String' }],
    output: 'String',
    colour: 230,
    tooltip: 'Ask the user for input',
    helpUrl: '',
  },
  {
    type: 'python_str_concat',
    message0: '%1 + %2',
    args0: [
      { type: 'input_value', name: 'A' },
      { type: 'input_value', name: 'B' },
    ],
    output: 'String',
    colour: 230,
    tooltip: 'Concatenate two values as strings',
    helpUrl: '',
  },
  {
    type: 'python_cast',
    message0: 'cast %1 to %2',
    args0: [
      { type: 'input_value', name: 'VALUE' },
      {
        type: 'field_dropdown',
        name: 'TYPE',
        options: [
          ['int', 'int'],
          ['float', 'float'],
          ['str', 'str'],
          ['bool', 'bool'],
        ],
      },
    ],
    output: null,
    colour: 230,
    tooltip: 'Cast a value to int, float, str, or bool',
    helpUrl: '',
  },
]);
