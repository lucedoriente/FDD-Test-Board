import os, re
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Transistor_FET.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()
matches = [m for m in re.findall(r'\(symbol\s+"([^"]+)"', text) if "AO3401" in m or "SI2319" in m or "DMP3098" in m or "P-MOS" in m]
print("Found P-MOSFETs:", matches)
