import os
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Amplifier_Current.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "INA180A1" in line:
        for l in lines[max(0, i-2):min(len(lines), i+35)]:
            print(l, end="")
        break
