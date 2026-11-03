import pcbnew

pcb_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad\FDD-Test-Board.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

for fp in board.GetFootprints():
    if "Mounting" in str(fp.GetFPID().GetLibItemName()):
        bb_full = fp.GetBoundingBox(True, True)
        bb_body = fp.GetBoundingBox(False, False)
        print(f"Mounting hole at ({fp.GetPosition().x/1e6:.1f}, {fp.GetPosition().y/1e6:.1f}):")
        print(f"  Full BB: left={bb_full.GetLeft()/1e6:.1f}, right={bb_full.GetRight()/1e6:.1f}, top={bb_full.GetTop()/1e6:.1f}, bottom={bb_full.GetBottom()/1e6:.1f}")
        print(f"  Body BB: left={bb_body.GetLeft()/1e6:.1f}, right={bb_body.GetRight()/1e6:.1f}, top={bb_body.GetTop()/1e6:.1f}, bottom={bb_body.GetBottom()/1e6:.1f}")
        for t in fp.GraphicalItems():
            print("  Graphic:", t.GetLayerName(), t.GetBoundingBox().GetLeft()/1e6, t.GetBoundingBox().GetRight()/1e6)
        break
