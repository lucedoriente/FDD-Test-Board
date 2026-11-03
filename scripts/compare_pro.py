import json

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_pro", "r", encoding="utf-8") as f:
    ic_pro = json.load(f)

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pro", "r", encoding="utf-8") as f:
    fdd_pro = json.load(f)

print("IC-Test-Board erc severities:")
print(json.dumps(ic_pro.get("schematic", {}).get("erc", {}).get("severities", {}), indent=2))

print("FDD-Test-Board erc severities:")
print(json.dumps(fdd_pro.get("schematic", {}).get("erc", {}).get("severities", {}), indent=2))
