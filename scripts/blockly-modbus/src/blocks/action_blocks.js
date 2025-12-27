import * as Blockly from 'blockly/core';

const modbus_pull_data = {
    type: 'modbus_pull_data',
    message0: 'Pull Data Config: %1',
    args0: [
        {
            type: 'input_value',
            name: 'CONFIG',
            check: 'ModbusConfig'
        }
    ],
    output: 'Array', // or 'None' depending on implementation preference, allows connecting to get_field
    colour: 230,
    tooltip: 'Executes the Modbus request using the provided configuration.',
    helpUrl: ''
};

const set_modbus_interval = {
    type: 'set_modbus_interval',
    message0: 'Set Poll Interval (ms): %1',
    args0: [
        {
            type: 'input_value',
            name: 'INTERVAL_MS',
            check: 'Number'
        }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 230,
    tooltip: 'Sets the frequency of Modbus polling in milliseconds.',
    helpUrl: ''
};

const modbus_get_field = {
    type: 'modbus_get_field',
    message0: 'Get %1 from %2',
    args0: [
        {
            type: 'field_dropdown',
            name: 'FIELD',
            options: [
                ['Raw Hex', 'raw'],
                ['Slave ID', 'slave_id'],
                ['Registers', 'registers'],
                ['Error', 'error']
            ]
        },
        {
            type: 'input_value',
            name: 'DATA',
            check: ['Array', 'Object'] // Accepts the output of pull_data
        }
    ],
    output: null,
    colour: 230,
    tooltip: 'Extracts a specific field from the Modbus result.',
    helpUrl: ''
};

const modbus_task_definition = {
    type: 'modbus_task_definition',
    message0: 'Task %1 (Interval %2s) %3 %4',
    args0: [
        { type: 'field_input', name: 'TASK_ID', text: '01' },
        { type: 'field_number', name: 'INTERVAL', value: 15, min: 1 },
        { type: 'input_dummy' },
        { type: 'input_statement', name: 'DO' }
    ],
    colour: 120,
    tooltip: 'Defines a periodic task.',
    helpUrl: ''
};

const modbus_get_register = {
    type: 'modbus_get_register',
    message0: 'Get Register Index %1 from %2',
    args0: [
        { type: 'input_value', name: 'INDEX', check: 'Number' },
        { type: 'input_value', name: 'DATA', check: ['Array', 'Object'] }
    ],
    output: null,
    colour: 230,
    tooltip: 'Gets a value from the registers list by index.',
    helpUrl: ''
};

const modbus_get_limiter = {
    type: 'modbus_get_limiter',
    message0: 'Get Limiter %1',
    args0: [
        { type: 'field_input', name: 'LIMITER_NAME', text: 'DP_Limit_LV1' }
    ],
    output: 'Number',
    colour: 230,
    tooltip: 'Retrieves the value of a specific limiter.',
    helpUrl: ''
};

const modbus_dcp_update = {
    type: 'modbus_dcp_update',
    message0: 'DCP Update %1 = %2',
    args0: [
        { type: 'field_input', name: 'NAME', text: 'LPS02___X' },
        { type: 'input_value', name: 'VALUE' }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 160,
    tooltip: 'Updates a value in the DCP system.',
    helpUrl: ''
};

const modbus_alarm_evaluator = {
    type: 'modbus_alarm_evaluator',
    message0: 'Eval Alarm Val: %1 LV1: %2 LV2: %3 LV3: %4',
    args0: [
        { type: 'input_value', name: 'VAL', check: 'Number' },
        { type: 'input_value', name: 'LV1', check: 'Number' },
        { type: 'input_value', name: 'LV2', check: 'Number' },
        { type: 'input_value', name: 'LV3', check: 'Number' }
    ],
    output: 'String',
    colour: 210,
    tooltip: 'Returns LV1/LV2/LV3/LV0 based on value thresholds.',
    helpUrl: ''
};

const modbus_log = {
    type: 'modbus_log',
    message0: 'Log %1',
    args0: [
        { type: 'input_value', name: 'MSG' }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: 65,
    tooltip: 'Logs a message.',
    helpUrl: ''
};

Blockly.defineBlocksWithJsonArray([
    modbus_pull_data,
    set_modbus_interval,
    modbus_get_field,
    modbus_task_definition,
    modbus_get_register,
    modbus_get_limiter,
    modbus_dcp_update,
    modbus_alarm_evaluator,
    modbus_log
]);
