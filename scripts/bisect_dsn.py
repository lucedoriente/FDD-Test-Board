import pcbnew, subprocess, sys, os

board = pcbnew.LoadBoard(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb")
refs = [fp.GetReference() for fp in board.GetFootprints()]

prefixes = sorted(list(set(''.join([c for c in r if c.isalpha()]) for r in refs)))
print("Prefixes:", prefixes)

runner = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\test_single_pfx.py"

for pfx in prefixes:
    with open(runner, "w") as f:
        f.write(f'''import pcbnew
board = pcbnew.LoadBoard(r"C:\\Users\\aless\\OneDrive\\temp\\Manutenzione\\Kicad_Project\\FDD_Tester\\kicad\\FDD-Test-Board.kicad_pcb")
b = pcbnew.BOARD()
b.SetCopperLayerCount(4)
for d in board.GetDrawings():
    if d.GetLayer() == pcbnew.Edge_Cuts:
        b.Add(d.Duplicate())
for fp in board.GetFootprints():
    if fp.GetReference().startswith("{pfx}"):
        b.Add(fp.Duplicate())
ok = pcbnew.ExportSpecctraDSN(b, r"C:\\Users\\aless\\OneDrive\\temp\\Manutenzione\\Kicad_Project\\FDD_Tester\\kicad\\test_pfx.dsn")
print(ok)
''')
    try:
        res = subprocess.run([r"C:\Program Files\KiCad\9.0\bin\python.exe", runner], capture_output=True, text=True, timeout=5)
        print(f"Prefix {pfx:4s}: stdout={res.stdout.strip()} stderr={res.stderr.strip()}")
    except subprocess.TimeoutExpired:
        print(f"Prefix {pfx:4s}: TIMEOUT (BLOCKED)")
