import os, re

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single\01_Power_Supply.kicad_sch", "r") as f:
    text = f.read()

# Find all instantiated symbols in body
idx = text.find('\n  (symbol (lib_id')
body = text[idx:]
syms = re.findall(r'\(symbol \(lib_id "([^"]+)"\)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+\d+\).*?\(property "Reference" "([^"]+)"', body, re.DOTALL)
print(f"Total symbols in body: {len(syms)}")
for lid, x, y, ref in syms:
    print(f"  {ref} ({lid}) at ({x}, {y})")
