
export const forBlock = Object.create(null);

forBlock['RTU_config'] = function (block, generator) {
  const Order = generator.ORDER_ATOMIC || 0; 
  
  const port = block.getFieldValue('PORT');
  const baudrate = block.getFieldValue('BAUDRATE');
  const start_address = block.getFieldValue('START_ADDRESS');
  const count = block.getFieldValue('COUNT');
  const function_code = block.getFieldValue('FUNCTION_CODE');
  const slave_id = block.getFieldValue('SLAVE_ID');

  const code = `RTUConfig(
    port="${port}",
    baudrate=${baudrate},
    start_address=${start_address},
    count=${count},
    function_code=${function_code},
    slave_id=${slave_id}
)`;
  return [code, Order]; 
};

forBlock['TCP_config'] = function (block, generator) {
  const Order = generator.ORDER_ATOMIC || 0;

  const host = block.getFieldValue('HOST');
  const port = block.getFieldValue('PORT');
  const start_address = block.getFieldValue('START_ADDRESS');
  const count = block.getFieldValue('COUNT');
  const function_code = block.getFieldValue('FUNCTION_CODE');

  const code = `connection_type.TCPConfig(
    host="${host}",
    port=${port},
    start_address=${start_address},
    count=${count},
    function_code=${function_code}
)`;
  return [code, Order];
};