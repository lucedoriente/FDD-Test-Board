import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch", "r", encoding="utf-8") as f:
    s4 = f.read()

# search for 73.66 or 147.32
for line in s4.splitlines():
    if "73.66" in line or "147.32" in line:
        print(line)
