import os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_sch", "r", encoding="utf-8") as f:
    ic = f.read()

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch", "r", encoding="utf-8") as f:
    fdd = f.read()

print("IC length:", len(ic), "FDD length:", len(fdd))
print("\nIC content:\n", ic)
print("\nFDD content:\n", fdd)
