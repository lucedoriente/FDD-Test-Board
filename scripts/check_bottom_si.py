import os

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in ["02_MCU_Core.kicad_sch", "03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]:
    p = os.path.join(prj_dir, f)
    with open(p, "r", encoding="utf-8") as file:
        t = file.read()
    idx = t.rfind('(sheet_instances')
    print(f"=== {f} ===")
    print(t[idx:])
