import os

p_ic = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\02_MCU_Core.kicad_sch"
p_fdd = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch"

with open(p_ic, "r", encoding="utf-8") as f:
    text_ic = f.read()

with open(p_fdd, "r", encoding="utf-8") as f:
    text_fdd = f.read()

lines_ic = text_ic.split("\n")
lines_fdd = text_fdd.split("\n")

print("IC lines 1-20:")
print("\n".join(lines_ic[:20]))
print("\nFDD lines 1-20:")
print("\n".join(lines_fdd[:20]))

print("\nIC last 20 lines:")
print("\n".join(lines_ic[-20:]))
print("\nFDD last 20 lines:")
print("\n".join(lines_fdd[-20:]))
