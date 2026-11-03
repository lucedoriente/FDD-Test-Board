import subprocess, os, re

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

with open(os.path.join(prj_dir, "01_Power_Supply.kicad_sch"), "r", encoding="utf-8") as f:
    full_ps = f.read()

# Make sure root points to 01_Power_Supply.kicad_sch
root_sch = """(kicad_sch
  (version 20250114)
  (generator "eeschema")
  (generator_version "9.0")
  (uuid "b20a3201-1001-4001-8001-000000000001")
  (paper "A3")
  (lib_symbols
  )
  (sheet (at 25.4 38.1) (size 63.5 25.4)
    (stroke (width 0.1524) (type solid))
    (fill (color 255 255 255 0.0000))
    (uuid "b20a3201-1001-4001-8001-000000000002")
    (property "Sheetname" "Power_Supply" (at 25.4 36.83 0) (effects (font (size 1.27 1.27)) (justify left bottom)))
    (property "Sheetfile" "01_Power_Supply.kicad_sch" (at 25.4 64.77 0) (effects (font (size 1.27 1.27)) (justify left top)))
    (instances
      (project "FDD-Test-Board"
        (path "/b20a3201-1001-4001-8001-000000000001"
          (page "2")
        )
      )
    )
  )
  (sheet_instances
    (path "/"
      (page "1")
    )
  )
)
"""
with open(os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "w", encoding="utf-8") as f:
    f.write(root_sch)

# Test 1: ONLY J1 in 01_Power_Supply.kicad_sch
with open(os.path.join(test_dir, "sub.kicad_sch"), "r", encoding="utf-8") as f:
    sub_j1 = f.read()

with open(os.path.join(test_dir, "01_Power_Supply.kicad_sch"), "w", encoding="utf-8") as f:
    f.write(sub_j1)

out_f = os.path.join(test_dir, "test_s1_step1.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
with open(out_f, "r", encoding="utf-8") as f:
    txt = f.read()

comps = re.findall(r'\(comp \(ref "([^"]+)"\)', txt)
print(f"Step 1 (J1 only in 01_Power_Supply): {len(comps)} comps -> {comps}")
