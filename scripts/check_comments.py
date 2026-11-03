import os, re

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in ["01_Power_Supply.kicad_sch", "02_MCU_Core.kicad_sch", "03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]:
    p = os.path.join(prj_dir, f)
    with open(p, "r", encoding="utf-8") as file:
        lines = file.readlines()
    comments = [l.strip() for l in lines if l.strip().startswith(';')]
    print(f"{f}: {len(comments)} comment lines found")
    for c in comments[:5]:
        print("  ", c)
