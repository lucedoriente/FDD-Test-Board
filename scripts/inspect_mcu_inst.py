import os
p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('(symbol (lib_id "MCU_ST_STM32F4:STM32F407VETx"')
if start != -1:
    print(text[start:start+500])
