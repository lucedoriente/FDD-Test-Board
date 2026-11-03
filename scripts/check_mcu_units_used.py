import os, re
p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

units = re.findall(r'\(symbol\s+\(lib_id\s+\"MCU_ST_STM32F4:STM32F407VETx\"\)[^\)]*\(unit\s+(\d+)\)', text)
print("Units used for STM32F407 in IC-Test-Board:", units)
