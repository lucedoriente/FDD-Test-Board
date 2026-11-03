import os
p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('STM32F407')
if start != -1:
    print(text[max(0, start-100):min(len(text), start+300)])
