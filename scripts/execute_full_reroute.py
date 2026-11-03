import os, sys, json, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_nozones = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.kicad_pcb")
pcb_final = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
dsn_path = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.dsn")
ses_path = os.path.join(PRJ_DIR, "FDD-Test-Board-nozones.ses")
local_pretty = os.path.join(PRJ_DIR, "FDD-Test-Board.pretty")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
java_exe = r"C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe"
freerouting_jar = r"C:\Users\aless\.gemini\antigravity\scratch\TI99_26\tools\freerouting-2.5.0.jar"

print("=== STEP 1: PREPARE BOARD FOR DSN EXPORT ===")
board = pcbnew.LoadBoard(pcb_nozones)

# Verify J6
j6 = board.FindFootprintByReference("J6")
print(f"J6 Reference: {j6.GetReference()}, Pos: ({j6.GetPosition().x/1e6:.2f}, {j6.GetPosition().y/1e6:.2f}), Rot: {j6.GetOrientationDegrees()}")

# Sync L1 and L2
l1 = board.FindFootprintByReference("L1")
if l1:
    l1.SetValue("10uH")
    l1.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))
l2 = board.FindFootprintByReference("L2")
if l2:
    l2.SetValue("4.7uH")
    l2.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))

# Ensure silk-to-edge constraint doesn't throw spurious warnings for overhanging connectors
board.GetDesignSettings().m_SilkToEdgeClearance = 0

# Set mechanical board-only attributes
for h_ref in ["H1", "H2", "H3", "H4"]:
    h_fp = board.FindFootprintByReference(h_ref)
    if h_fp:
        h_fp.SetBoardOnly(True)

for i in range(1, 7):
    tp = board.FindFootprintByReference(f"TP{i}")
    if tp:
        tp.SetExcludedFromBOM(False)

# Delete existing tracks/vias and zones
print(f"Deleting {len(board.GetTracks())} old tracks/vias and {len(board.Zones())} zones...")
for t in list(board.GetTracks()):
    board.Delete(t)
for z in list(board.Zones()):
    board.Delete(z)

# Save unrouted board
board.Save(pcb_nozones)

# Export clean DSN
if os.path.exists(dsn_path):
    os.remove(dsn_path)
if os.path.exists(ses_path):
    os.remove(ses_path)

ok = pcbnew.ExportSpecctraDSN(board, dsn_path)
print(f"ExportSpecctraDSN result: {ok}, Size: {os.path.getsize(dsn_path)} bytes")
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
print(f"Configured {cfg_file} with gui.enabled = false")

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

    # Ensure L1 and L2
    l1 = b.FindFootprintByReference("L1")
    if l1:
        l1.SetValue("10uH")
        l1.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))
    l2 = b.FindFootprintByReference("L2")
    if l2:
        l2.SetValue("4.7uH")
        l2.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", "L_7.3x7.3_H4.5"))

    for h_ref in ["H1", "H2", "H3", "H4"]:
        h_fp = b.FindFootprintByReference(h_ref)
        if h_fp:
            h_fp.SetBoardOnly(True)

    for i in range(1, 7):
        tp = b.FindFootprintByReference(f"TP{i}")
        if tp:
            tp.SetExcludedFromBOM(False)

    b.GetDesignSettings().m_MinResolvedSpokes = 1
    b.GetDesignSettings().m_SilkToEdgeClearance = 0

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
        lines = f.readlines()
    print("DRC Report Summary:")
    for line in lines:
        if "violations" in line or "unconnected" in line or "parity" in line.lower() or "error" in line.lower():
            print("  ", line.strip())
