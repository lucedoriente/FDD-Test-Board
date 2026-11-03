import pcbnew
import os

pcb_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

fps = list(board.GetFootprints())
print(f"Total footprints on board: {len(fps)}")

overlaps = []
for i in range(len(fps)):
    fp1 = fps[i]
    ref1 = fp1.GetReference()
    bb1 = fp1.GetBoundingBox(True, True)
    for j in range(i + 1, len(fps)):
        fp2 = fps[j]
        ref2 = fp2.GetReference()
        bb2 = fp2.GetBoundingBox(True, True)
        if bb1.Intersects(bb2):
            # Calculate intersection
            inter = bb1
            overlaps.append((ref1, ref2, bb1, bb2))

print(f"Total bounding box intersections: {len(overlaps)}")
for r1, r2, b1, b2 in overlaps[:20]:
    print(f"  Overlap between {r1} and {r2}")
