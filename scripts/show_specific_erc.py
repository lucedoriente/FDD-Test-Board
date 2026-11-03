import os, re

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
if not os.path.exists(rpt_path):
    rpt_path = "FDD-Test-Board-erc.rpt"

with open(rpt_path, "r", encoding="utf-8") as f:
    text = f.read()

for section in text.split("["):
    if not section.strip(): continue
    tag = section[:section.find("]")] if "]" in section else ""
    if tag in ["lib_symbol_mismatch", "footprint_link_issues", "power_pin_not_driven", "multiple_net_names", "pin_to_pin"]:
        print(f"[{section.strip()}\n" + "-"*50)
