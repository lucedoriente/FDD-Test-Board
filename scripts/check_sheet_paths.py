import os, re

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
for f, sheet_uuid in [
    ("01_Power_Supply.kicad_sch", "b20a3201-1001-4001-8001-000000000002"),
    ("02_MCU_Core.kicad_sch", "b20a3201-1001-4001-8001-000000000003"),
    ("03_UI_Controls.kicad_sch", "b20a3201-1001-4001-8001-000000000004"),
    ("04_FDD_Interfaces.kicad_sch", "b20a3201-1001-4001-8001-000000000005"),
]:
    p = os.path.join(prj_dir, f)
    with open(p, "r", encoding="utf-8") as file:
        t = file.read()
    # Find all path entries in instances
    paths = set(re.findall(r'\(path "([^"]+)"', t))
    print(f"{f}: {len(paths)} unique paths:")
    for path in sorted(list(paths)):
        print("  ", path)
