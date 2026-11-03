import subprocess, os

test_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\test_single"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

out_f = os.path.join(test_dir, "test_dbg.net")
res = subprocess.run([kicad_cli, "sch", "export", "netlist", os.path.join(test_dir, "FDD-Test-Board.kicad_sch"), "-o", out_f], capture_output=True, text=True)
print("RC:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
