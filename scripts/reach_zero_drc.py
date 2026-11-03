import pcbnew, os, subprocess

PRJ_DIR = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
kicad_cli = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
pcb_path = os.path.join(PRJ_DIR, "FDD-Test-Board.kicad_pcb")
local_pretty = os.path.join(PRJ_DIR, "FDD-Test-Board.pretty")

board = pcbnew.LoadBoard(pcb_path)

# 1. H1..H4: SetBoardOnly(True) per fori meccanici da telaio
for ref in ["H1", "H2", "H3", "H4"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetBoardOnly(True)

# 2. Sincronizzazione perfetta libreria locale per J10, J11, J12, J13
fp_map = {
    "J10": "IDC-Header_2x25_P2.54mm_Horizontal",
    "J11": "IDC-Header_2x17_P2.54mm_Horizontal",
    "J12": "IDC-Header_2x13_P2.54mm_Horizontal",
    "J13": "IDC-Header_2x10_P2.54mm_Horizontal"
}
for ref, fpname in fp_map.items():
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetFPID(pcbnew.LIB_ID("FDD-Test-Board", fpname))
        pcbnew.FootprintSave(local_pretty, fp)

# 3. Riempimento Zone e salvataggio
filler = pcbnew.ZONE_FILLER(board)
filler.Fill(board.Zones())

board.Save(pcb_path)
print("Board sincronizzata e salvata.")

# 4. DRC finale KiCad 9 con schematic-parity
drc_rpt = os.path.join(PRJ_DIR, "FDD-Test-Board-drc-final-report.rpt")
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "--severity-all", "--output", drc_rpt, pcb_path]
res = subprocess.run(cmd, capture_output=True, text=True)
print("=== DRC RESULT ===")
print("Exit Code:", res.returncode)
with open(drc_rpt, "r", encoding="utf-8") as f:
    text = f.read()
print(text)
