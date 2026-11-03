import subprocess, os, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
fdd_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"

with open(os.path.join(fdd_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    ps_content = f.read()

# Let's see: in test_single, we have FDD-Test-Board.kicad_sch pointing to sub.kicad_sch.
# We know sub.kicad_sch with R1 works!
# Let's take sub.kicad_sch:
# Header:
hdr = ps_content[:ps_content.find('(symbol (lib_id ')]
footer = """  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""

# Extract all symbol blocks:
sym_matches = list(re.finditer(r'  \(symbol \(lib_id.*?\n    \)\n  \)', ps_content, re.DOTALL))
print(f"Total symbol blocks in 01_Power_Supply: {len(sym_matches)}")

# Test adding N symbols to sub.kicad_sch
def test_symbols(count):
    body = "\n".join([m.group(0) for m in sym_matches[:count]])
    sub_text = hdr + body + "\n" + footer
    with open(os.path.join(test_dir, "sub.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(sub_text)
    cmd = [r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe", "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", os.path.join(test_dir, "test_b.net")]
    res = subprocess.run(cmd, capture_output=True, text=True)
    with open(os.path.join(test_dir, "test_b.net"), "r", encoding="utf-8") as f:
        net = f.read()
    comps = re.findall(r'\(comp \(ref "([^"]+)"\)', net)
    return len(comps), res.returncode

print("Test with 1 symbol:")
c, rc = test_symbols(1)
print(f"Comps exported: {c}, RC: {rc}")
print("First symbol reference:", re.search(r'\(property "Reference" "([^"]+)"', sym_matches[0].group(0)).group(1))

print("Test with 5 symbols:")
c, rc = test_symbols(5)
print(f"Comps exported: {c}, RC: {rc}")

print("Test with all symbols:")
c, rc = test_symbols(len(sym_matches))
print(f"Comps exported: {c}, RC: {rc}")
