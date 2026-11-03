import os, re

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "MCU_ST_STM32F4.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

# Check extends
target = '(symbol "STM32F407VETx"'
idx = text.find(target)
chunk = text[idx:idx+2000]
print(chunk[:500])
