import os

rpt_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board-erc.rpt"
with open(rpt_path, "r", encoding="utf-8") as f:
    text = f.read()

sheets = text.split("***** Sheet ")
for s in sheets[1:]:
    sheet_name = s.splitlines()[0]
    lines = s.splitlines()[1:]
    v_lines = [l for l in lines if l.startswith("[")]
    print(f"Sheet {sheet_name}: {len(v_lines)} violations")
    for v in v_lines[:5]:
        print("  ", v)
