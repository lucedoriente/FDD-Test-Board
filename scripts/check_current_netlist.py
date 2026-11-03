import os, re

net_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.net"
with open(net_path, "r", encoding="utf-8") as f:
    text = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', text)
nets = re.findall(r'\(net \(code "[^"]+"\)\s+\(name "([^"]+)"\)', text)
print(f"Netlist length: {len(text)}")
print(f"Components in netlist: {len(comps)}")
print(f"Nets in netlist: {len(nets)}")
print("Sample components:", comps[:30])
