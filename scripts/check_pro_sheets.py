import os, json

p_ic = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_pro"
p_fdd = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pro"

with open(p_ic, "r", encoding="utf-8") as f:
    j_ic = json.load(f)

with open(p_fdd, "r", encoding="utf-8") as f:
    j_fdd = json.load(f)

print("IC schematic settings:", j_ic.get("schematic", {}))
print("FDD schematic settings:", j_fdd.get("schematic", {}))
