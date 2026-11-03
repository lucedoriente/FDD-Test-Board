import os, difflib

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    working = f.readlines()

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    orig = f.readlines()

diff = list(difflib.unified_diff(orig, working, fromfile='original', tofile='working', n=3))
print(f"Total diff lines: {len(diff)}")
for line in diff[:100]:
    print(line, end='')
