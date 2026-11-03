import os

p_ic = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\01_Power_Supply.kicad_sch"
p_fdd = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch"

with open(p_ic, "r", encoding="utf-8") as f:
    text_ic = f.read()

with open(p_fdd, "r", encoding="utf-8") as f:
    text_fdd = f.read()

print("IC sheet 1 lines 1-10:")
print("\n".join(text_ic.split("\n")[:10]))

print("\nFDD sheet 1 lines 1-10:")
print("\n".join(text_fdd.split("\n")[:10]))
