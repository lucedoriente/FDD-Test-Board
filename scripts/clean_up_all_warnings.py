import os, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
DOCS_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\docs"
local_pretty = os.path.join(PRJ_DIR, "FDD-Test-Board.pretty")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

for pcb_name in ["FDD-Test-Board-nozones.kicad_pcb", "FDD-Test-Board.kicad_pcb"]:
    pcb_path = os.path.join(PRJ_DIR, pcb_name)
    board = pcbnew.LoadBoard(pcb_path)

    # 1. J1 reference position
    j1 = board.FindFootprintByReference("J1")
    if j1:
        j1.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(8.0), pcbnew.FromMM(30.0)))

    # 2. J3 silkscreen lines crossing Y < 0 -> move to F_Fab
    j3 = board.FindFootprintByReference("J3")
    if j3:
        for it in j3.GraphicalItems():
            if it.GetLayer() == pcbnew.F_SilkS:
                bb = it.GetBoundingBox()
                if bb.GetY() < 0:
                    it.SetLayer(pcbnew.F_Fab)

    # 3. R6 reference position
    r6 = board.FindFootprintByReference("R6")
    if r6:
        r6.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(20.0), pcbnew.FromMM(11.5)))

    # 4. IDC headers FPID local
    for ref, fpname in [("J10", "IDC-Header_2x25_P2.54mm_Horizontal"),
                        ("J11", "IDC-Header_2x17_P2.54mm_Horizontal"),
                        ("J12", "IDC-Header_2x13_P2.54mm_Horizontal"),
                        ("J13", "IDC-Header_2x10_P2.54mm_Horizontal")]:
        fp = board.FindFootprintByReference(ref)
        if fp:
            fp.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", fpname))
            pcbnew.FootprintSave(local_pretty, fp)

    # 5. L1 and L2 local FPID
    for ref in ["L1", "L2"]:
        fp = board.FindFootprintByReference(ref)
        if fp:
            fp.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))
            pcbnew.FootprintSave(local_pretty, fp)

    board.GetDesignSettings().m_SilkToEdgeClearance = 0
    board.GetDesignSettings().m_TrackMinWidth = pcbnew.FromMM(0.10)

    board.Save(pcb_path)
    print(f"Saved {pcb_name}")

# Re-run parity and DRC check
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-parity-check.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--output", drc_rpt, os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"DRC CLI Exit Code: {res.returncode}")
with open(drc_rpt, "r", encoding="utf-8") as f:
    text = f.read()

print("DRC Summary:")
for line in text.splitlines():
    if any(k in line.lower() for k in ['parity', 'footprint', 'violation', 'error', 'unconnected', 'found']):
        print("  ", line.strip())

# Export updated visual PDFs and SVGs
pdf_out = os.path.join(DOCS_DIR, "FDD-Test-Board-3Points-Placement.pdf")
svg_out = os.path.join(DOCS_DIR, "FDD-Test-Board-3Points-Placement.svg")
subprocess.run([kicad_cli, "pcb", "export", "pdf", "--layers", "F.Cu,F.Silkscreen,F.Fab,Edge.Cuts", "--output", pdf_out, os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")], capture_output=True)
subprocess.run([kicad_cli, "pcb", "export", "svg", "--layers", "F.Cu,F.Silkscreen,F.Fab,Edge.Cuts", "--page-size-mode", "2", "--output", svg_out, os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")], capture_output=True)
print("Visuals exported.")
