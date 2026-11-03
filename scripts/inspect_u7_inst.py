import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\02_MCU_Core.kicad_sch"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

u7_matches = re.findall(r'\(symbol \(lib_id "([^"]+)"\)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+\d+\)\s+\(unit\s+(\d+)\).*?\(property "Reference" "U7"', text, re.DOTALL)
print(f"U7 instances found: {len(u7_matches)}")
for m in u7_matches:
    print(m)
