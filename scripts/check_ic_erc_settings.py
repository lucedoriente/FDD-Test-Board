import json

with open(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_pro", "r") as f:
    data = json.load(f)

erc = data.get("erc", {}).get("rule_severities", {})
print("lib_symbol_mismatch in IC-Test-Board:", erc.get("lib_symbol_mismatch"))
print("All erc rule severities in IC-Test-Board:")
for k, v in erc.items():
    if v != "error":
        print(f"  {k}: {v}")
