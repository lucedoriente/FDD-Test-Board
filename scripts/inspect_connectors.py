import os, re
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
with open(os.path.join(prj_dir, "FDD-Test-Board.net"), "r", encoding="utf-8") as f:
    text = f.read()
for j in ["J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9", "J10", "J11", "J12", "J13", "J14"]:
    m = re.search(r'\(comp \(ref "' + j + r'"\).*?\(footprint "([^"]+)"\)', text, re.DOTALL)
    if m:
        print(f"{j}: {m.group(1)}")
