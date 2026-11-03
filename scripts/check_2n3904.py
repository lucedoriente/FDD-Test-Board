import os

sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
p = os.path.join(sym_dir, "Transistor_BJT.kicad_sym")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(symbol "2N3904"')
print(text[idx:idx+300])
