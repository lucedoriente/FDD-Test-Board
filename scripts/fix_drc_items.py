import os, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

for p in [pcb_path, pcb_nozones]:
    board = pcbnew.LoadBoard(p)
    # 1. Fix thin tracks (< 0.12mm)
    min_w = pcbnew.FromMM(0.12)
    fixed_tracks = 0
    for t in board.GetTracks():
        if not isinstance(t, pcbnew.PCB_VIA) and t.GetWidth() < min_w:
            t.SetWidth(pcbnew.FromMM(0.15))
            fixed_tracks += 1
    print(f"Fixed {fixed_tracks} thin tracks in {os.path.basename(p)}")

    # 2. Fix J10, J11, J12, J13 silk crossing board edge -> move to F_Fab
    fixed_silk = 0
    for ref in ['J10', 'J11', 'J12', 'J13']:
        fp = board.FindFootprintByReference(ref)
        if fp:
            for it in fp.GraphicalItems():
                if it.GetLayer() == pcbnew.F_SilkS:
                    # Move to F_Fab so it doesn't clip Edge.Cuts
                    it.SetLayer(pcbnew.F_Fab)
                    fixed_silk += 1
    print(f"Moved {fixed_silk} silkscreen items to F_Fab in {os.path.basename(p)}")

    # Refill zones
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(p)

print("\nRunning DRC verification...")
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"DRC Exit Code: {res.returncode}")
with open(drc_rpt, "r", encoding="utf-8") as f:
    text = f.read()
print(text)
