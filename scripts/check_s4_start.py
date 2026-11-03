import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\04_FDD_Interfaces.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

print("\n".join(text.split("\n")[:25]))
