import os, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

board = pcbnew.LoadBoard(pcb_path)
print(f"Tracce presenti sulla scheda: {len(board.GetTracks())}")
print(f"Zone presenti prima del riempimento: {len(board.Zones())}")

# Se le zone non ci sono ancora, le aggiungiamo
if len(board.Zones()) == 0:
    gnd_net = board.FindNet("GND")
    vcc_net = board.FindNet("+5V_REG")
    W, H = 200.0, 140.0
    inset = 0.5

    def add_plane(net_obj, layer_id, name):
        if not net_obj: return
        z = pcbnew.ZONE(board)
        z.SetNet(net_obj)
        z.SetZoneName(name)
        lset = pcbnew.LSET()
        lset.AddLayer(layer_id)
        z.SetLayerSet(lset)
        z.SetLayer(layer_id)
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        z.SetMinThickness(pcbnew.FromMM(0.15))
        z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.20))
        z.SetThermalReliefGap(pcbnew.FromMM(0.20))
        poly = pcbnew.SHAPE_LINE_CHAIN()
        for px, py in [(inset, inset), (W - inset, inset), (W - inset, H - inset), (inset, H - inset)]:
            poly.Append(pcbnew.FromMM(px), pcbnew.FromMM(py))
        poly.SetClosed(True)
        z.AddPolygon(poly)
        board.Add(z)

    add_plane(gnd_net, pcbnew.In1_Cu, "GND_PLANE_IN1")
    add_plane(vcc_net, pcbnew.In2_Cu, "VCC_5V_PLANE_IN2")
    print("Zone GND e +5V_REG aggiunte.")

# Impostazioni meccaniche e parità
for h_ref in ["H1", "H2", "H3", "H4"]:
    h_fp = board.FindFootprintByReference(h_ref)
    if h_fp:
        h_fp.SetBoardOnly(True)

for i in range(1, 7):
    tp = board.FindFootprintByReference(f"TP{i}")
    if tp:
        tp.SetExcludedFromBOM(False)

board.GetDesignSettings().m_MinResolvedSpokes = 1

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
print("Piani di rame riempiti con successo.")

board.Save(pcb_path)
print(f"Scheda salvata su {pcb_path}.")

# Esecuzione DRC
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print("=== DRC ESITO ===")
print("Exit Code:", res.returncode)
with open(drc_rpt, "r", encoding="utf-8") as f:
    text = f.read()
print(text)
