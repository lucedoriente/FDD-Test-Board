import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\test.net"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('(comp (ref "U1"')
print(text[idx:idx+400])
