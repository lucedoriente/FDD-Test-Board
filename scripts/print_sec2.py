import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

sections = text.split(';; --- ')
print("Section 2 (J1):")
print(sections[1])
