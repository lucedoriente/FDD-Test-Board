import os, sys, json, subprocess
import pcbnew

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
dsn_path = os.path.join(PRJ_DIR, "FDD-Test-Board.dsn")
ses_path = os.path.join(PRJ_DIR, "FDD-Test-Board.ses")
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
java_exe = r"C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe"
freerouting_jar = r"C:\Users\aless\AppData\Local\freerouting\app\freerouting-executable.jar"

if not os.path.exists(freerouting_jar):
    freerouting_jar = r"C:\Users\aless\.gemini\antigravity\scratch\TI99_26\tools\freerouting-2.5.0.jar"

print(f"=== FDD MASTER TESTER ROUTING EXECUTION ===")
print(f"DSN: {dsn_path} ({os.path.getsize(dsn_path)} bytes)")

# 1. Force Headless in freerouting.json
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

print("1. Freerouting configurato in modalità HEADLESS.")

# 2. Run Freerouting
print("2. Esecuzione autorouter Freerouting batch...")
cmd = [java_exe, "-jar", freerouting_jar, "-de", dsn_path, "-do", ses_path, "-mp", "30"]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"   Return code: {res.returncode}")
if res.returncode != 0:
    print("   STDOUT:", res.stdout)
    print("   STDERR:", res.stderr)
    sys.exit(1)

print(f"   SES generato: {ses_path} ({os.path.getsize(ses_path)} bytes)")

# 3. Import SES into KiCad PCB
print("3. Importazione file SES nella PCB KiCad 9...")
board = pcbnew.LoadBoard(pcb_path)
for t in list(board.GetTracks()):
    board.Remove(t)

ok = pcbnew.ImportSpecctraSES(board, ses_path)
print(f"   ImportSpecctraSES: {ok}")
print(f"   Tracce caricate: {len(board.GetTracks())}")

# 4. Aggiunta Piani di Rame (GND e +5V_REG) e riempimento
print("4. Aggiunta piani interni di rame (In1.Cu GND, In2.Cu +5V_REG)...")
gnd_net = board.FindNet("GND")
vcc_net = board.FindNet("+5V_REG")

W, H = 200.0, 140.0
inset = 0.5

def add_plane(net_obj, layer_id, name):
    if not net_obj:
        return
    z = pcbnew.ZONE(board)
    z.SetNet(net_obj)
    z.SetZoneName(name)
    lset = pcbnew.LSET()
    lset.AddLayer(layer_id)
    z.SetLayerSet(lset)
    z.SetLayer(layer_id)
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    z.SetMinThickness(pcbnew.FromMM(0.15))
    z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.25))
    z.SetThermalReliefGap(pcbnew.FromMM(0.25))
    poly = pcbnew.SHAPE_LINE_CHAIN()
    for px, py in [(inset, inset), (W - inset, inset), (W - inset, H - inset), (inset, H - inset)]:
        poly.Append(pcbnew.FromMM(px), pcbnew.FromMM(py))
    poly.SetClosed(True)
    z.AddPolygon(poly)
    board.Add(z)

add_plane(gnd_net, pcbnew.In1_Cu, "GND_PLANE_IN1")
add_plane(vcc_net, pcbnew.In2_Cu, "VCC_5V_PLANE_IN2")

filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())
print("   Piani di rame riempiti con successo.")

board.Save(pcb_path)
print(f"   Scheda salvata su {pcb_path}.")

# 5. DRC KiCad 9
print("5. Esecuzione DRC con schematic parity check...")
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final.rpt")
drc_cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
drc_res = subprocess.run(drc_cmd, capture_output=True, text=True)
print(f"   DRC Exit code: {drc_res.returncode}")
print(drc_res.stdout)
