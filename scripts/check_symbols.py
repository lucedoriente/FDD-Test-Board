import os
import re

p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Mechanical.kicad_sym"
if os.path.exists(p):
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()
    symbols = [m for m in re.findall(r'\(symbol\s+"([^"]+)"', text) if "MountingHole" in m]
    print("Found symbols:", symbols)
