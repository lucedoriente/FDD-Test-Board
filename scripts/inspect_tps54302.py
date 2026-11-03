import os
p = r"C:\Program Files\KiCad\9.0\share\kicad\symbols\Regulator_Switching.kicad_sym"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('(symbol "TPS54302"')
end = text.find('\n  )', start)
if start != -1:
    print(text[start:end+4])
