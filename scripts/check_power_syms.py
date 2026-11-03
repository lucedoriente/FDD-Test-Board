import os

kicad_sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
with open(os.path.join(kicad_sym_dir, "power.kicad_sym"), "r", encoding="utf-8") as f:
    text = f.read()

print("Is +24V in power.kicad_sym?", '+24V' in text)
print("Is -12V in power.kicad_sym?", '-12V' in text)
print("Is -12VA in power.kicad_sym?", '-12VA' in text)
print("Is -5V in power.kicad_sym?", '-5V' in text)
print("Is +12V in power.kicad_sym?", '+12V' in text)
