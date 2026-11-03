import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    s2 = f.read()

# find all wires touching x=121.92
wires = re.findall(r'\(wire \(pts \(xy [^\)]+\) \(xy [^\)]+\)\)[^\)]*\)', s2)
for w in wires:
    if "121.92" in w:
        print("Wire at 121.92:", w)
