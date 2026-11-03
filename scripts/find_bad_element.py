import pcbnew, subprocess, sys, os

# Script che prova a rimuovere ciascun footprint da una copia della board e testare ExportSpecctraDSN
runner = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\test_delete_ref.py"

board = pcbnew.LoadBoard(r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb")
refs = [fp.GetReference() for fp in board.GetFootprints()]

# Testiamo rimuovendo blocchi per vedere quale blocco rimuovendo sblocca l'export
chunk_size = 15
for k in range(0, len(refs), chunk_size):
    chunk = refs[k:k+chunk_size]
    with open(runner, "w") as f:
        f.write(f'''import pcbnew, sys
board = pcbnew.LoadBoard(r"C:\\Users\\aless\\OneDrive\\temp\\Manutenzione\\Kicad_Project\\FDD_Tester\\kicad\\FDD-Test-Board.kicad_pcb")
for z in list(board.Zones()):
    board.Remove(z)
chunk = {chunk!r}
for r in chunk:
    fp = board.FindFootprintByReference(r)
    if fp:
        board.Delete(fp)
ok = pcbnew.ExportSpecctraDSN(board, r"C:\\Users\\aless\\OneDrive\\temp\\Manutenzione\\Kicad_Project\\FDD_Tester\\kicad\\test_chunk.dsn")
print("SUCCESS:", ok)
''')
    try:
        res = subprocess.run([r"C:\Program Files\KiCad\9.0\bin\python.exe", runner], capture_output=True, text=True, timeout=3)
        if "SUCCESS: True" in res.stdout:
            print(f"Chunk {k//chunk_size} (refs {chunk[0]}..{chunk[-1]}): REMOVING THIS CHUNK SUCCEEDED! The culprit is in this chunk!")
            break
        else:
            print(f"Chunk {k//chunk_size} (refs {chunk[0]}..{chunk[-1]}): Failed/Blocked (stdout: {res.stdout.strip()[:30]})")
    except subprocess.TimeoutExpired:
        print(f"Chunk {k//chunk_size} (refs {chunk[0]}..{chunk[-1]}): TIMEOUT (still blocked)")
