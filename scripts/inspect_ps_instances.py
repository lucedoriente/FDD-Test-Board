import os, re, subprocess

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps_content = f.read()

# Let's see all symbol instances in ps_content:
sym_matches = list(re.finditer(r'\(symbol \(lib_id "([^"]+)"\)', ps_content))
print(f"Total symbol instances in 01_Power_Supply: {len(sym_matches)}")
refs = re.findall(r'\(property "Reference" "([^"]+)"', ps_content)
print(f"Refs in 01_Power_Supply: {refs}")

# Let's check the (instances ...) block of each symbol in ps_content!
inst_blocks = re.findall(r'\(symbol \(lib_id "[^"]+"\).*?\n    \(instances(.*?)\n    \)', ps_content, re.DOTALL)
print(f"Total instances blocks in 01_Power_Supply: {len(inst_blocks)}")
for i, b in enumerate(inst_blocks[:5]):
    print(f"Instance {i}: {b.strip()}")
