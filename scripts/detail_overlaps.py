import pcbnew, os

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(prj_dir, "FDD-Test-Board.kicad_pcb")
board = pcbnew.LoadBoard(pcb_path)

fps = list(board.GetFootprints())
print(f"Total footprints: {len(fps)}")

overlaps = []
for i in range(len(fps)):
    fp1 = fps[i]
    ref1 = fp1.GetReference()
    pos1 = fp1.GetPosition()
    bb1 = fp1.GetBoundingBox(False, False)
    
    for j in range(i + 1, len(fps)):
        fp2 = fps[j]
        ref2 = fp2.GetReference()
        pos2 = fp2.GetPosition()
        bb2 = fp2.GetBoundingBox(False, False)
        
        if bb1.Intersects(bb2):
            overlaps.append((ref1, pos1, bb1, ref2, pos2, bb2))

print(f"Total overlaps: {len(overlaps)}")
for r1, p1, b1, r2, p2, b2 in overlaps:
    print(f"Overlap between {r1} @ ({pcbnew.ToMM(p1.x):.1f}, {pcbnew.ToMM(p1.y):.1f}) [X:{pcbnew.ToMM(b1.GetLeft()):.1f}..{pcbnew.ToMM(b1.GetRight()):.1f}, Y:{pcbnew.ToMM(b1.GetTop()):.1f}..{pcbnew.ToMM(b1.GetBottom()):.1f}]")
    print(f"            and {r2} @ ({pcbnew.ToMM(p2.x):.1f}, {pcbnew.ToMM(p2.y):.1f}) [X:{pcbnew.ToMM(b2.GetLeft()):.1f}..{pcbnew.ToMM(b2.GetRight()):.1f}, Y:{pcbnew.ToMM(b2.GetTop()):.1f}..{pcbnew.ToMM(b2.GetBottom()):.1f}]")
    print()
