import re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.net"
txt = open(p, encoding="utf-8").read()

comps = re.findall(r'\(comp\s+\(ref\s+"([^"]+)"\)', txt)
nets = re.findall(r'\(net\s+\(code\s+"[^"]+"\)\s+\(name\s+"([^"]+)"\)', txt)

print(f"Total components in netlist: {len(comps)}")
print(f"Total nets in netlist: {len(nets)}")
print(f"First 10 comps: {comps[:10]}")
print(f"Power nets: {[n for n in nets if any(k in n for k in ['24V', '12V', '5V', '3.3V', 'GND'])]}")
