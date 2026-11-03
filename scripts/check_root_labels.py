import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

labels = re.findall(r'\(label "([^"]+)"', text)
glabels = re.findall(r'\(global_label "([^"]+)"', text)
wires = re.findall(r'\(wire', text)
print(f"Root sheet has {len(labels)} labels, {len(glabels)} global_labels, {len(wires)} wires")
