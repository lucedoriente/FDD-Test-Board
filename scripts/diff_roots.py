import os, re

# Compare sheet blocks in root
p_ic = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_sch"
p_fdd = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch"

with open(p_ic, "r", encoding="utf-8") as f:
    text_ic = f.read()

with open(p_fdd, "r", encoding="utf-8") as f:
    text_fdd = f.read()

print("IC sheet 1 block:")
idx_ic = text_ic.find('(sheet ')
idx_ic_end = text_ic.find('(sheet ', idx_ic+1)
print(text_ic[idx_ic:idx_ic_end])

print("\nFDD sheet 1 block:")
idx_fdd = text_fdd.find('(sheet ')
idx_fdd_end = text_fdd.find('(sheet ', idx_fdd+1)
print(text_fdd[idx_fdd:idx_fdd_end])
