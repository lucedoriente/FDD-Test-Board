import pcbnew

pcb_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)
fps = list(board.GetFootprints())

real_overlaps = []
for i in range(len(fps)):
    fp1 = fps[i]
    ref1 = fp1.GetReference()
    bb1 = fp1.GetBoundingBox(False, False)
    for j in range(i + 1, len(fps)):
        fp2 = fps[j]
        ref2 = fp2.GetReference()
        bb2 = fp2.GetBoundingBox(False, False)
        if bb1.Intersects(bb2):
            pos1 = fp1.GetPosition()
            pos2 = fp2.GetPosition()
            real_overlaps.append((ref1, ref2, pos1, pos2))

print(f"Total REAL physical overlaps: {len(real_overlaps)}")
for r1, r2, p1, p2 in real_overlaps:
    print(f"  {r1} at ({p1.x/1e6:.1f}, {p1.y/1e6:.1f}) <-> {r2} at ({p2.x/1e6:.1f}, {p2.y/1e6:.1f})")
