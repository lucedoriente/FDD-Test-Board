import os

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
with open(rpt_path, "r", encoding="utf-8") as f:
    text = f.read()

sheets = text.split("***** Sheet ")
for s in sheets[1:]:
    sheet_name = s.splitlines()[0]
    if "MCU" in sheet_name or "UI" in sheet_name or "FDD" in sheet_name:
        continue
    print(f"=== Sheet {sheet_name} ===")
    for l in s.splitlines()[1:]:
        print(l)
