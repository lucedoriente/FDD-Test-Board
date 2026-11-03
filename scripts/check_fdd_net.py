import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.net"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', text)
nets = re.findall(r'\(net \(code "([^"]+)"\) \(name "([^"]+)"\)', text)
print(f"NETLIST RESULT: {len(comps)} components, {len(nets)} nets!")
print("Sample components:", comps[:15])
