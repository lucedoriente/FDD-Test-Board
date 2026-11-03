import subprocess, os, re

fdd_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

with open(os.path.join(fdd_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps_content = f.read()

refs = re.findall(r'\(property "Reference" "([^"]+)"', ps_content)
print(f"Total references in 01_Power_Supply: {len(refs)}")
print("Refs:", refs)
