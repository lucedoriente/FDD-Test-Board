import re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\01_Power_Supply.kicad_sch", "r", encoding="utf-8") as f:
    s1 = f.read()

# Let's find labels / global_labels in Sheet 1 and their exact coordinates
glabels = re.findall(r'\(global_label "([^"]+)" [^\(]*\(at ([0-9\.-]+) ([0-9\.-]+)', s1)
for name, x, y in glabels:
    print(f"Global label {name} at ({x}, {y})")

labels = re.findall(r'\(label "([^"]+)" \(at ([0-9\.-]+) ([0-9\.-]+)', s1)
for name, x, y in labels:
    if any(k in name for k in ["24V", "12V", "5V", "GND"]):
        print(f"Label {name} at ({x}, {y})")
