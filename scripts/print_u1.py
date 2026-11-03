import os
p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('(property "Reference" "U1"')
if start != -1:
    sym_start = text.rfind('(symbol ', 0, start)
    print(text[sym_start:sym_start+600])
