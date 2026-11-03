import pcbnew, os, subprocess

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

board = pcbnew.LoadBoard(pcb_path)

# 1. Sincronizzazione TP1..TP6
for i in range(1, 7):
    tp = board.FindFootprintByReference(f"TP{i}")
    if tp:
        tp.SetExcludedFromBOM(False)

# 2. Sincronizzazione H1..H4 con path KIID di root
for i, (hx, hy) in enumerate([(5.0, 5.0), (195.0, 5.0), (195.0, 135.0), (5.0, 135.0)], 1):
    h = board.FindFootprintByReference(f"H{i}")
    if h:
        h.SetPath(pcbnew.KIID_PATH(f"/b20a3201-1001-4001-8001-0000000000{i:02d}"))
        h.SetExcludedFromBOM(False)

# 3. Zone Settings: raggio termico e spoke count
ds = board.GetDesignSettings()
ds.m_MinResolvedSpokes = 1

for z in board.Zones():
    z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.20))
    z.SetThermalReliefGap(pcbnew.FromMM(0.20))

# 4. Risoluzione silkscreen clipped: linee di serigrafia che escono da Edge.Cuts spostate su F.Fab
W, H = 200.0, 140.0
for ref in ["J10", "J11", "J12", "J13"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        for gi in fp.GraphicalItems():
            if gi.GetLayer() == pcbnew.F_SilkS:
                bb = gi.GetBoundingBox()
                if bb.GetLeft() < 0 or bb.GetRight() > pcbnew.FromMM(W) or bb.GetTop() < 0 or bb.GetBottom() > pcbnew.FromMM(H):
                    gi.SetLayer(pcbnew.F_Fab)

# 5. Riempimento Zone
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

board.Save(pcb_path)
print("PCB Finalizzata e Salvata.")

# 6. Esecuzione DRC KiCad 9 con schematic parity
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print("=== DRC RESULT ===")
print("Exit Code:", res.returncode)
print(res.stdout)
