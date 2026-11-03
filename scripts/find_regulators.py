import os, re
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Regulator_Switching.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()
matches = [m for m in re.findall(r'\(symbol\s+"([^"]+)"', text) if "TPS543" in m or "TPS542" in m or "LM2596" in m]
print("Found regulators:", matches)
