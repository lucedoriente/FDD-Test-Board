import os, re
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\74xx.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()
matches = [m for m in re.findall(r'\(symbol\s+"([^"]+)"', text) if "74LS06" in m or "74ACT06" in m or "7406" in m or "7414" in m or "74LS14" in m]
print("Found 74xx symbols:", matches[:10])
