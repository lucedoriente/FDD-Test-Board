import os, re

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\test.net"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', text)
print("Components in IC-Test-Board test.net:", len(comps))
