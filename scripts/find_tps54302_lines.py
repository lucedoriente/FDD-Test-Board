import os
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Regulator_Switching.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "TPS54302" in line:
        for l in lines[max(0, i-5):min(len(lines), i+35)]:
            print(l, end="")
        break
