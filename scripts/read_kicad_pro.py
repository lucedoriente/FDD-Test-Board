import os

p = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pro"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

print("Length of kicad_pro:", len(text))
for line in text.split("\n")[:40]:
    print(line)
