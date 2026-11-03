import pcbnew, os

prj_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(prj_dir, "FDD-Test-Board.kicad_pcb")
board = pcbnew.LoadBoard(pcb_path)

print(f"{'Ref':<6} {'Val':<15} {'X (mm)':<8} {'Y (mm)':<8} {'Rot':<6} {'BBox X (mm)':<20} {'BBox Y (mm)':<20}")
print("-" * 85)

for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref.startswith("J") or ref.startswith("SW") or ref in ["U5", "BZ1"]:
        pos = fp.GetPosition()
        rot = fp.GetOrientation().AsDegrees()
        bb = fp.GetBoundingBox(False, False)
        val = fp.GetValue()
        bx_str = f"[{pcbnew.ToMM(bb.GetLeft()):.1f}..{pcbnew.ToMM(bb.GetRight()):.1f}]"
        by_str = f"[{pcbnew.ToMM(bb.GetTop()):.1f}..{pcbnew.ToMM(bb.GetBottom()):.1f}]"
        print(f"{ref:<6} {val:<15} {pcbnew.ToMM(pos.x):<8.1f} {pcbnew.ToMM(pos.y):<8.1f} {rot:<6.0f} {bx_str:<20} {by_str:<20}")
