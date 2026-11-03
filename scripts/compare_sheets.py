import os, re

ic_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad"
fdd_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

with open(os.path.join(ic_dir, "IC-Test-Board.kicad_sch"), "r", encoding="utf-8") as f:
    ic_sch = f.read()

with open(os.path.join(fdd_dir, "FDD-Test-Board.kicad_sch"), "r", encoding="utf-8") as f:
    fdd_sch = f.read()

# Let's inspect the sheets definitions in both
sheets_ic = re.findall(r'\(sheet \(at [^\)]+\) \(size [^\)]+\).*?\n  \)', ic_sch, re.DOTALL)
sheets_fdd = re.findall(r'\(sheet \(at [^\)]+\) \(size [^\)]+\).*?\n  \)', fdd_sch, re.DOTALL)

print("IC sheets count:", len(sheets_ic))
for s in sheets_ic:
    name = re.search(r'\(property "Sheetname" "([^"]+)"', s).group(1)
    file = re.search(r'\(property "Sheetfile" "([^"]+)"', s).group(1)
    uuid = re.search(r'\(uuid "([^"]+)"', s).group(1)
    print(f"  IC Sheet: {name} -> {file} (uuid: {uuid})")

print("\nFDD sheets count:", len(sheets_fdd))
for s in sheets_fdd:
    name = re.search(r'\(property "Sheetname" "([^"]+)"', s).group(1)
    file = re.search(r'\(property "Sheetfile" "([^"]+)"', s).group(1)
    uuid = re.search(r'\(uuid "([^"]+)"', s).group(1)
    print(f"  FDD Sheet: {name} -> {file} (uuid: {uuid})")
