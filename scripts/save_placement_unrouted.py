import os, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
DOCS_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\docs"
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
pcb_final = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

for pcb_file in [pcb_nozones, pcb_final]:
    board = pcbnew.LoadBoard(pcb_file)

    # 1. Clear existing tracks and zones for unrouted placement
    for t in list(board.GetTracks()):
        board.Delete(t)
    for z in list(board.Zones()):
        board.Delete(z)

    # 2. J1 (24V IN from internal Mean Well PSU) -> on left edge facing PSU
    j1 = board.FindFootprintByReference("J1")
    if j1:
        j1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(6.5), pcbnew.FromMM(32.0)))
        j1.SetOrientationDegrees(90.0)

    # 3. J6 (USB Type-C) -> on rear edge Y=0
    j6 = board.FindFootprintByReference("J6")
    if j6:
        j6.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(16.5), pcbnew.FromMM(4.35)))
        j6.SetOrientationDegrees(180.0)

    # 4. USB cluster (D1, R4, R5, R6, R7)
    d1 = board.FindFootprintByReference("D1")
    if d1:
        d1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(16.5), pcbnew.FromMM(13.5)))
        d1.SetOrientationDegrees(0.0)

    r4 = board.FindFootprintByReference("R4")
    if r4:
        r4.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(13.0), pcbnew.FromMM(13.5)))
        r4.SetOrientationDegrees(90.0)

    r5 = board.FindFootprintByReference("R5")
    if r5:
        r5.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(13.0), pcbnew.FromMM(17.0)))
        r5.SetOrientationDegrees(90.0)

    r6 = board.FindFootprintByReference("R6")
    if r6:
        r6.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(20.0), pcbnew.FromMM(13.5)))
        r6.SetOrientationDegrees(90.0)

    r7 = board.FindFootprintByReference("R7")
    if r7:
        r7.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(20.0), pcbnew.FromMM(17.0)))
        r7.SetOrientationDegrees(90.0)

    # 5. J3 (3.5" Berg power connector) -> moved forward to Y=8.5mm, pins extend to Y=-1.6mm
    j3 = board.FindFootprintByReference("J3")
    if j3:
        j3.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(52.0), pcbnew.FromMM(8.5)))
        j3.SetOrientationDegrees(90.0)

    # 6. Ensure mechanical attributes
    for href in ["H1", "H2", "H3", "H4"]:
        h = board.FindFootprintByReference(href)
        if h:
            h.SetBoardOnly(True)

    for i in range(1, 7):
        tp = board.FindFootprintByReference(f"TP{i}")
        if tp:
            tp.SetExcludedFromBOM(False)

    board.GetDesignSettings().m_SilkToEdgeClearance = 0
    board.GetDesignSettings().m_TrackMinWidth = pcbnew.FromMM(0.10)

    board.Save(pcb_file)
    print(f"Saved unrouted placement: {os.path.basename(pcb_file)}")

# Export visuals
pdf_out = os.path.join(DOCS_DIR, "FDD-Test-Board-Placement-Unrouted.pdf")
svg_out = os.path.join(DOCS_DIR, "FDD-Test-Board-Placement-Top.svg")

subprocess.run([kicad_cli, "pcb", "export", "pdf", "--layers", "F.Cu,F.Silkscreen,F.Fab,Edge.Cuts", "--output", pdf_out, pcb_final], capture_output=True)
subprocess.run([kicad_cli, "pcb", "export", "svg", "--layers", "F.Cu,F.Silkscreen,F.Fab,Edge.Cuts", "--page-size-mode", "2", "--output", svg_out, pcb_final], capture_output=True)

print(f"Exported PDF: {pdf_out}")
print(f"Exported SVG: {svg_out}")
