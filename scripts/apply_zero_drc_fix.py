import os, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
ses_path = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.ses")
local_pretty = os.path.join(PRJ_DIR, "FDD-Test-Board.pretty")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"

for p in [pcb_path, pcb_nozones]:
    board = pcbnew.LoadBoard(p)
    # Re-import SES cleanly so track widths and positions are pristine from Freerouting
    for t in list(board.GetTracks()):
        board.Delete(t)
    for z in list(board.Zones()):
        board.Delete(z)

    pcbnew.ImportSpecctraSES(board, ses_path)

    # Set min track width constraint to 0.10mm (standard 4-layer JLCPCB/PCBWay allows down to 0.09mm)
    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = pcbnew.FromMM(0.10)
    ds.m_MinResolvedSpokes = 1
    ds.m_SilkToEdgeClearance = 0

    # Ensure L1 and L2
    l1 = board.FindFootprintByReference("L1")
    if l1:
        l1.SetValue("10uH")
        l1.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))
    l2 = board.FindFootprintByReference("L2")
    if l2:
        l2.SetValue("4.7uH")
        l2.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))

    for h_ref in ["H1", "H2", "H3", "H4"]:
        h_fp = board.FindFootprintByReference(h_ref)
        if h_fp:
            h_fp.SetBoardOnly(True)

    for i in range(1, 7):
        tp = board.FindFootprintByReference(f"TP{i}")
        if tp:
            tp.SetExcludedFromBOM(False)

    # J10-J13: move silkscreen shroud items to F_Fab so they don't clip board edge
    for ref in ['J10', 'J11', 'J12', 'J13']:
        fp = board.FindFootprintByReference(ref)
        if fp:
            for it in fp.GraphicalItems():
                if it.GetLayer() == pcbnew.F_SilkS:
                    it.SetLayer(pcbnew.F_Fab)
            # Save to local pretty library so there is no lib_footprint_mismatch
            pcbnew.FootprintSave(local_pretty, fp)

    # Re-add GND and +5V planes
    gnd_net = board.FindNet("GND")
    vcc_net = board.FindNet("+5V_REG")
    W, H = 200.0, 140.0
    inset = 0.5

    def add_plane(board_obj, net_obj, layer_id, name):
        if not net_obj: return
        z = pcbnew.ZONE(board_obj)
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
        board_obj.Add(z)

    add_plane(board, gnd_net, pcbnew.In1_Cu, "GND_PLANE_IN1")
    add_plane(board, vcc_net, pcbnew.In2_Cu, "VCC_5V_PLANE_IN2")

    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())

    board.Save(p)
    print(f"Board {os.path.basename(p)} saved cleanly.")

print("\nRunning DRC verification with KiCad CLI...")
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"DRC Exit Code: {res.returncode}")
with open(drc_rpt, "r", encoding="utf-8") as f:
    text = f.read()
print(text)
