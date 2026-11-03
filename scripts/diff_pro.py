import json, os

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_pro", "r") as f:
    pic = json.load(f)

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pro", "r") as f:
    pfdd = json.load(f)

print("IC keys:", pic.keys())
print("FDD keys:", pfdd.keys())

for k in pic.keys():
    if k not in pfdd:
        print("Missing in FDD:", k)
    elif pic[k] != pfdd[k]:
        print(f"Key {k} differs")
