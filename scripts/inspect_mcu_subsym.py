import os
from test_flatten_engine import get_flattened_symbol

mcu_flat = get_flattened_symbol("MCU_ST_STM32F4", "STM32F407VETx")
idx = mcu_flat.find('STM32F407VETx_1_1')
print(mcu_flat[idx:idx+500])
