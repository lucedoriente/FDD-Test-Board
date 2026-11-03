import os, sys, json, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
DOCS_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\docs"
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
pcb_final = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
dsn_path = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.dsn")
ses_path = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.ses")
local_pretty = os.path.join(PRJ_DIR, "FDD-Test-Board.pretty")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
java_exe = r"C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe"
freerouting_jar = r"C:\Users\aless\.gemini\antigravity\scratch\TI99_26\tools\freerouting-2.5.0.jar"

print("=== STEP 1: EXPORT DSN FOR FREEROUTING ===")
board = pcbnew.LoadBoard(pcb_nozones)

# Ensure design settings
ds = board.GetDesignSettings()
ds.m_TrackMinWidth = pcbnew.FromMM(0.10)
ds.m_SilkToEdgeClearance = 0
ds.m_MinResolvedSpokes = 1

for h_ref in ["H1", "H2", "H3", "H4"]:
    h = board.FindFootprintByReference(h_ref)
    if h:
        h.SetBoardOnly(True)

for i in range(1, 7):
    tp = board.FindFootprintByReference(f"TP{i}")
    if tp:
        tp.SetExcludedFromBOM(False)

board.Save(pcb_nozones)

if os.path.exists(dsn_path):
    os.remove(dsn_path)
if os.path.exists(ses_path):
    os.remove(ses_path)

ok = pcbnew.ExportSpecctraDSN(board, dsn_path)
print(f"ExportSpecctraDSN result: {ok}, Size: {os.path.getsize(dsn_path) if os.path.exists(dsn_path) else 0} bytes")
if not ok:
    print("ERROR: Failed to export DSN!")
    sys.exit(1)

print("\n=== STEP 2: CONFIGURE FREEROUTING HEADLESS ===")
cfg_dir = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp", "freerouting")
os.makedirs(cfg_dir, exist_ok=True)
cfg_file = os.path.join(cfg_dir, "freerouting.json")
with open(cfg_file, "w", encoding="utf-8") as f:
    json.dump({
        "profile": {
            "id": "b14c330b-0443-4b67-a2f2-1a42532cb7b2",
            "email": "alessio67@gmail.com",
            "allow_telemetry": False,
            "allow_contact": False
        },
        "gui": {
            "enabled": False
        }
    }, f, indent=2)
print("Configured freerouting.json with gui.enabled = false")

print("\n=== STEP 3: RUN FREEROUTING AUTOROUTER ===")
cmd = [java_exe, "-jar", freerouting_jar, "-de", dsn_path, "-do", ses_path, "-mp", "30"]
print("Executing:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Freerouting return code: {res.returncode}")
if res.returncode != 0:
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    sys.exit(1)

if not os.path.exists(ses_path):
    print("ERROR: SES file was not generated!")
    sys.exit(1)

print(f"SES file generated successfully: {ses_path} ({os.path.getsize(ses_path)} bytes)")

print("\n=== STEP 4: IMPORT SES AND POPULATE PLANES ===")
for target_pcb in [pcb_nozones, pcb_final]:
    print(f"Importing SES into {os.path.basename(target_pcb)}...")
    b = pcbnew.LoadBoard(target_pcb)
    for t in list(b.GetTracks()):
        b.Delete(t)
    for z in list(b.Zones()):
        b.Delete(z)

    import_ok = pcbnew.ImportSpecctraSES(b, ses_path)
    print(f"ImportSpecctraSES: {import_ok}, Tracks imported: {len(b.GetTracks())}")

    b_ds = b.GetDesignSettings()
    b_ds.m_TrackMinWidth = pcbnew.FromMM(0.10)
    b_ds.m_SilkToEdgeClearance = 0
    b_ds.m_MinResolvedSpokes = 1

    for h_ref in ["H1", "H2", "H3", "H4"]:
        h = b.FindFootprintByReference(h_ref)
        if h:
            h.SetBoardOnly(True)

    for i in range(1, 7):
        tp = b.FindFootprintByReference(f"TP{i}")
        if tp:
            tp.SetExcludedFromBOM(False)

    # Add GND and +5V planes
    gnd_net = b.FindNet("GND")
    vcc_net = b.FindNet("+5V_REG")
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

    add_plane(b, gnd_net, pcbnew.In1_Cu, "GND_PLANE_IN1")
    add_plane(b, vcc_net, pcbnew.In2_Cu, "VCC_5V_PLANE_IN2")

    filler = pcbnew.ZONE_FILLER(b)
    filler.Fill(b.Zones())

    b.Save(target_pcb)
    print(f"Saved: {target_pcb}")

print("\n=== STEP 5: RUN KICAD-CLI DRC & SCHEMATIC PARITY ===")
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_final]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"DRC CLI Exit Code: {res.returncode}")
if os.path.exists(drc_rpt):
    with open(drc_rpt, "r", encoding="utf-8") as f:
        text = f.read()
    print("=== DRC REPORT ===")
    print(text)

# Export updated visual documentation
print("\n=== STEP 6: EXPORT DOCUMENTATION ===")
pdf_out = os.path.join(DOCS_DIR, "FDD-Test-Board-Routed.pdf")
svg_top = os.path.join(DOCS_DIR, "FDD-Test-Board-Routed-Top.svg")
svg_bottom = os.path.join(DOCS_DIR, "FDD-Test-Board-Routed-Bottom.svg")

subprocess.run([kicad_cli, "pcb", "export", "pdf", "--layers", "F.Cu,B.Cu,In1.Cu,In2.Cu,F.Silkscreen,B.Silkscreen,Edge.Cuts", "--output", pdf_out, pcb_final], capture_output=True)
subprocess.run([kicad_cli, "pcb", "export", "svg", "--layers", "F.Cu,F.Silkscreen,Edge.Cuts", "--page-size-mode", "2", "--output", svg_top, pcb_final], capture_output=True)
subprocess.run([kicad_cli, "pcb", "export", "svg", "--layers", "B.Cu,B.Silkscreen,Edge.Cuts", "--page-size-mode", "2", "--output", svg_bottom, pcb_final], capture_output=True)
print("Documentation exported successfully.")
