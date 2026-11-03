import os, re

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f in ["02_MCU_Core.kicad_sch", "03_UI_Controls.kicad_sch", "04_FDD_Interfaces.kicad_sch"]:
    p = os.path.join(prj_dir, f)
    with open(p, "r", encoding="utf-8") as file:
        t = file.read()
    # find lines with path /b20a3201-1001-4001-8001-000000000001"
    matches = [m.start() for m in re.finditer(r'\(path "/b20a3201-1001-4001-8001-000000000001"\)', t)]
    print(f"{f}: {len(matches)} occurrences of root-only path")
    if matches:
        idx = matches[0]
        print("  Sample context:", t[idx-50:idx+80].replace('\n', ' '))
