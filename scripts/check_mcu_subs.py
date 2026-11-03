from test_flatten_engine import get_flattened_symbol, get_raw_sym_text
import re

raw = get_raw_sym_text("MCU_ST_STM32F4", "STM32F407V_E-G_Tx")
subs = re.findall(r'\(symbol "(STM32F407V_E-G_Tx_[^"]+)"', raw)
print("Raw parent sub-symbols:", subs)

flat = get_flattened_symbol("MCU_ST_STM32F4", "STM32F407VETx")
subs_flat = re.findall(r'\(symbol "(STM32F407VETx_[^"]+)"', flat)
print("Flattened sub-symbols:", subs_flat)
