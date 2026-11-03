import os, re
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Amplifier_Operational.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()
matches = [m for m in re.findall(r'\(symbol\s+"([^"]+)"', text) if "LM358" in m or "LMV358" in m or "OPA2350" in m or "OPA2365" in m]
print("Found OpAmps:", matches[:10])
