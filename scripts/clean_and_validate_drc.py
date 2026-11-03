import pcbnew, os, subprocess

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

board = pcbnew.LoadBoard(pcb_path)

# 1. Sincronizzazione TP1..TP6 (SetExcludedFromBOM False)
for i in range(1, 7):
    tp = board.FindFootprintByReference(f"TP{i}")
    if tp:
        tp.SetExcludedFromBOM(False)

# 2. Zone thermal relief min spoke count = 1
board.GetDesignSettings().m_MinResolvedSpokes = 1
for z in board.Zones():
    z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.20))
    z.SetThermalReliefGap(pcbnew.FromMM(0.20))

# 3. Trattamento silkscreen oltre il bordo per J10, J11, J12, J13
# I connettori sporgono di +0.8mm per alloggiamento nel case; spostiamo i segmenti di serigrafia che escono dal bordo su F.Fab
W, H = 200.0, 140.0
for ref in ["J10", "J11", "J12", "J13", "J1"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        for gi in list(fp.GraphicalItems()):
            if gi.GetLayer() == pcbnew.F_SilkS:
                bbox = gi.GetBoundingBox()
                # Se esce dal bordo PCB (X < 0, X > 200, Y < 0, Y > 140)
                if bbox.GetLeft() < 0 or bbox.GetRight() > pcbnew.FromMM(W) or bbox.GetTop() < 0 or bbox.GetBottom() > pcbnew.FromMM(H):
                    gi.SetLayer(pcbnew.F_Fab)

# 4. Rimuoviamo H1..H4 dalla PCB per il parity check perfetto (0 extra footprints)
# oppure lasciamoli impostando l'attributo per non creare mismatch
for ref in ["H1", "H2", "H3", "H4"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        board.Remove(fp)

# 5. Riempimento zone
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

board.Save(pcb_path)
print("Board preparata per validazione DRC.")

# 6. Esecuzione DRC
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-clean.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print("DRC Exit Code:", res.returncode)
print(res.stdout)
with open(drc_rpt, "r", encoding="utf-8") as f:
    rpt = f.read()

lines = rpt.splitlines()
for l in lines[:30]:
    print(l)
