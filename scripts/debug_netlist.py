import subprocess, os, re

ic_root = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\kicad\IC-Test-Board.kicad_sch"
fdd_root = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_sch"

with open(ic_root, 'r', encoding='utf-8') as f:
    tic = f.read()

with open(fdd_root, 'r', encoding='utf-8') as f:
    tfdd = f.read()

print("IC root sheet count:", tic.count('(sheet (at'))
print("FDD root sheet count:", tfdd.count('(sheet (at'))

# Let's see the exact text of sheet 1 in IC vs FDD
s_ic = re.search(r'\(sheet \(at 25\.4 38\.1\).*?\n  \)', tic, re.DOTALL).group(0)
s_fdd = re.search(r'\(sheet \(at 25\.4 38\.1\).*?\n  \)', tfdd, re.DOTALL).group(0)

print("\n--- IC sheet 1 ---")
print(s_ic)
print("\n--- FDD sheet 1 ---")
print(s_fdd)
