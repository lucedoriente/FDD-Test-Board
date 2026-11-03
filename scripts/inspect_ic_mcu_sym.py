import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

target = '(symbol "MCU_ST_STM32F4:STM32F407VETx"'
idx = text.find(target)
if idx != -1:
    print("Found symbol definition in lib_symbols! Length around:", len(text[idx:idx+2000]))
    print(text[idx:idx+500])
