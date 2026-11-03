import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\sub.kicad_sch", "r") as f:
    text = f.read()

print("Length of working sub.kicad_sch:", len(text))
print(text[:1000])
