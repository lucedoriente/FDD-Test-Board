import os, sys, json, subprocess, re
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

print(f"=== FDD MASTER TESTER ROUTING PIPELINE ===")
print(f"PCB: {pcb_path}")
print(f"Freerouting JAR: {freerouting_jar}")

# 1. Configurazione Headless Freerouting
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
print("1. Freerouting configurato in modalità HEADLESS (gui: false).")

# 2. Esportazione DSN
print("2. Esportazione Specctra DSN da KiCad PCB...")
board = pcbnew.LoadBoard(pcb_path)
for t in list(board.GetTracks()):
    board.Remove(t)

ok = pcbnew.ExportSpecctraDSN(board, dsn_path)
if not ok:
    print("ERRORE: ExportSpecctraDSN ha fallito!")
    sys.exit(1)
print(f"   DSN esportato con successo ({os.path.getsize(dsn_path)} bytes).")

# 3. Esecuzione Freerouting
print("3. Esecuzione autorouting con Freerouting (4 strati)...")
cmd = [java_exe, "-jar", freerouting_jar, "-de", dsn_path, "-do", ses_path, "-mp", "30"]
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"   Freerouting return code: {res.returncode}")
if res.returncode != 0:
    print("   Freerouting STDOUT:\n", res.stdout)
    print("   Freerouting STDERR:\n", res.stderr)
    sys.exit(1)

if not os.path.exists(ses_path) or os.path.getsize(ses_path) == 0:
    print("ERRORE: File SES non generato!")
    sys.exit(1)
print(f"   File SES generato con successo ({os.path.getsize(ses_path)} bytes).")

# 4. Importazione SES in KiCad
print("4. Importazione file SES in KiCad PCB...")
board = pcbnew.LoadBoard(pcb_path)
for t in list(board.GetTracks()):
    board.Remove(t)

import_ok = pcbnew.ImportSpecctraSES(board, ses_path)
print(f"   ImportSpecctraSES esito: {import_ok}")
print(f"   Tracce importate: {len(board.GetTracks())}")

# 5. Pulizia Dangling Vias & Riempimento Zone Rame
print("5. Riempimento e rigenerazione piani di rame...")
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

board.Save(pcb_path)
print(f"   Scheda salvata su {pcb_path}.")

# 6. Verifica DRC KiCad 9
print("6. Esecuzione DRC KiCad 9 con schematic parity check...")
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-routed-drc.rpt")
drc_cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
drc_res = subprocess.run(drc_cmd, capture_output=True, text=True)
print(f"   DRC Exit code: {drc_res.returncode}")
print(drc_res.stdout)
if drc_res.stderr:
    print(drc_res.stderr)
