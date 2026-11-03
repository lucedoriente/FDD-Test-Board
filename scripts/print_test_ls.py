import os, re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\test_ls.net", "r") as f:
    text = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', text)
print(f"Total comps in test_ls.net: {len(comps)}")
print("Comps:", comps)
