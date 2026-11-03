import os, subprocess, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    working_txt = f.read()

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    orig_txt = f.read()

# Let's compare lengths and differences
print("Working length:", len(working_txt))
print("Original length:", len(orig_txt))

# Let's test original file directly in test_dir:
with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
    f.write(orig_txt)

out_f = os.path.join(test_dir, "test_orig.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
with open(out_f, "r", encoding="utf-8") as f:
    txt = f.read()
comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
print(f"Original file exported: {len(comps)} comps -> {comps}")
