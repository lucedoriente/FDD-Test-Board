import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1 = f.read()

glabels = re.findall(r'\(global_label "([^"]+)" [^\(]*\(at ([0-9\.-]+) ([0-9\.-]+)', s1)
for name, x, y in glabels:
    print(f"Global label {name} at ({x}, {y})")
