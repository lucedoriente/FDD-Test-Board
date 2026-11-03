import os
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
pcb_final = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

for pcb_file in [pcb_nozones, pcb_final]:
    board = pcbnew.LoadBoard(pcb_file)

    # 1. Clear existing tracks and zones (user requested placement without routing)
    for t in list(board.GetTracks()):
        board.Delete(t)
    for z in list(board.Zones()):
        board.Delete(z)

    # 2. Adjust J3 (3.5" Berg power connector)
    # Move forward from Y=14.0 to Y=8.5 so pins extend 1.6mm past Edge.Cuts (Y = -1.6mm)
    j3 = board.FindFootprintByReference("J3")
    if j3:
        j3.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(52.0), pcbnew.FromMM(8.5)))
        j3.SetOrientationDegrees(90.0)

    # 3. Adjust J1 (24V IN Terminal block from internal Mean Well PSU)
    # Move to left edge facing internal Mean Well PSU on left
    j1 = board.FindFootprintByReference("J1")
    if j1:
        j1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(7.5), pcbnew.FromMM(25.0)))
        j1.SetOrientationDegrees(90.0)

    # 4. Move J6 (USB Type-C) to Rear Edge (Y=0)
    # X=16.5mm, Y=4.35mm, Rot=180 (mouth facing rear panel Y=0, pins facing inside board)
    j6 = board.FindFootprintByReference("J6")
    if j6:
        j6.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(16.5), pcbnew.FromMM(4.35)))
        j6.SetOrientationDegrees(180.0)

    # 5. Move USB cluster (D1, R4, R5, R6, R7) near J6
    d1 = board.FindFootprintByReference("D1")
    if d1:
        d1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(16.5), pcbnew.FromMM(11.0)))
        d1.SetOrientationDegrees(0.0)

    r4 = board.FindFootprintByReference("R4")
    if r4:
        r4.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(12.5), pcbnew.FromMM(11.0)))
        r4.SetOrientationDegrees(90.0)

    r5 = board.FindFootprintByReference("R5")
    if r5:
        r5.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(12.5), pcbnew.FromMM(15.0)))
        r5.SetOrientationDegrees(90.0)

    r6 = board.FindFootprintByReference("R6")
    if r6:
        r6.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(20.5), pcbnew.FromMM(11.0)))
        r6.SetOrientationDegrees(90.0)

    r7 = board.FindFootprintByReference("R7")
    if r7:
        r7.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(20.5), pcbnew.FromMM(15.0)))
        r7.SetOrientationDegrees(90.0)

    # Ensure H1..H4 board only
    for href in ["H1", "H2", "H3", "H4"]:
        h = board.FindFootprintByReference(href)
        if h:
            h.SetBoardOnly(True)

    board.Save(pcb_file)
    print(f"Updated placement saved in {os.path.basename(pcb_file)}")

print("Done updating placements.")
