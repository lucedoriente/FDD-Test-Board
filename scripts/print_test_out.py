import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_out.net"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

print(text[300:])
