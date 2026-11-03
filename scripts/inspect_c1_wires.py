import os, re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Find C1
idx = text.find('(property "Reference" "C1"')
s = text.rfind('(symbol ', 0, idx)
print("Symbol C1:")
print(text[s:idx+200])

# Find wires near (25.4, 45.72)
wires = re.findall(r'\(wire \(pts \(xy 25\.4.*?\n  \)', text)
print("\nWires near C1:")
for w in wires:
    print(w)
