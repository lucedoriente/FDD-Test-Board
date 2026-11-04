"""
Production Package Generator for KiCad 9.0 (100% JLCPCB / PCBWay Compliant)
Retro-Diag FDD Master Tester & Exerciser
Author: Alessio Iodice <alessio67@gmail.com>
License: CC BY-NC-SA 4.0
"""

import os
import sys
import shutil
import zipfile
import subprocess

KICAD_CLI = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"
PROJECT_ROOT = r"c:\Users\aless\.gemini\antigravity\scratch\FDD_Tester"
ONEDRIVE_ROOT = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester"

BOARDS = [
    {
        "name": "FDD-Test-Board",
        "title": "Mainboard",
        "sch": os.path.join(PROJECT_ROOT, "kicad", "FDD-Test-Board.kicad_sch"),
        "pcb": os.path.join(PROJECT_ROOT, "kicad", "FDD-Test-Board.kicad_pcb"),
        "layers": "F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts",
        "dest_dir": "FDD-Test-Board-Mainboard",
        "zip_prefix": "FDD-Test-Board_rev1.0"
    },
    {
        "name": "FDD_UI_Panel",
        "title": "Front-Panel",
        "sch": os.path.join(PROJECT_ROOT, "kicad", "FDD_UI_Panel", "FDD_UI_Panel.kicad_sch"),
        "pcb": os.path.join(PROJECT_ROOT, "kicad", "FDD_UI_Panel", "FDD_UI_Panel.kicad_pcb"),
        "layers": "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts",
        "dest_dir": "FDD_UI_Panel-FrontPanel",
        "zip_prefix": "FDD_UI_Panel_rev1.0"
    }
]

def run_cmd(args):
    print("Running:", " ".join(args))
    res = subprocess.run(args, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR:", res.stderr)
        print("STDOUT:", res.stdout)
        raise RuntimeError(f"Command failed with exit code {res.returncode}")
    return res.stdout

def create_board_package(board):
    print(f"\n========================================================")
    print(f"  Generating Production Package for: {board['name']} ({board['title']})")
    print(f"========================================================")
    
    prod_base = os.path.join(PROJECT_ROOT, "production", board["dest_dir"])
    gerber_dir = os.path.join(prod_base, "gerber")
    assembly_dir = os.path.join(prod_base, "assembly")
    reports_dir = os.path.join(prod_base, "validation_reports")
    
    if os.path.exists(gerber_dir): shutil.rmtree(gerber_dir)
    if os.path.exists(assembly_dir): shutil.rmtree(assembly_dir)
    if os.path.exists(reports_dir): shutil.rmtree(reports_dir)
    
    os.makedirs(gerber_dir, exist_ok=True)
    os.makedirs(assembly_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. Validation Reports (ERC & DRC)
    print("[1/5] Running Final ERC validation...")
    run_cmd([KICAD_CLI, "sch", "erc", "--output", os.path.join(reports_dir, f"{board['name']}_erc.rpt"), board["sch"]])
    
    print("[2/5] Running Final DRC & Parity validation...")
    run_cmd([KICAD_CLI, "pcb", "drc", "--schematic-parity", "--output", os.path.join(reports_dir, f"{board['name']}_drc.rpt"), board["pcb"]])

    # 2. Export Gerbers with standard .gbr naming (100% JLCPCB native compliant)
    print("[3/5] Exporting Gerber RS-274X layers (.gbr)...")
    run_cmd([
        KICAD_CLI, "pcb", "export", "gerbers",
        "--output", gerber_dir,
        "--layers", board["layers"],
        "--subtract-soldermask",
        "--no-protel-ext",
        "--no-x2",
        "--no-netlist",
        "--precision", "6",
        board["pcb"]
    ])
    
    # 3. Export Excellon Drill (Single unified file, no separate TH, no PDF map)
    print("[4/5] Exporting Unified Excellon Drill file (.drl)...")
    run_cmd([
        KICAD_CLI, "pcb", "export", "drill",
        "--output", gerber_dir + os.sep,
        "--format", "excellon",
        "--excellon-units", "mm",
        board["pcb"]
    ])
    
    # Clean any accidental job/pdf files from gerber directory
    for f in os.listdir(gerber_dir):
        if f.endswith('.gbrjob') or f.endswith('.pdf'):
            os.remove(os.path.join(gerber_dir, f))

    # 4. Export Assembly: Pick & Place (CPL / POS) and BOM
    print("[5/5] Exporting Component Placement List (CPL/POS) and BOM...")
    cpl_path = os.path.join(assembly_dir, f"{board['name']}_cpl.csv")
    run_cmd([
        KICAD_CLI, "pcb", "export", "pos",
        "--output", cpl_path,
        "--side", "both",
        "--format", "csv",
        "--units", "mm",
        board["pcb"]
    ])
    
    bom_path = os.path.join(assembly_dir, f"{board['name']}_bom.csv")
    run_cmd([
        KICAD_CLI, "sch", "export", "bom",
        "--output", bom_path,
        "--fields", "Reference,Value,Footprint,${QUANTITY}",
        "--labels", "Designator,Valore,Footprint,Quantita",
        "--group-by", "Value,Footprint",
        board["sch"]
    ])

    # 5. Create JLCPCB Compliant ZIP Archives
    gerber_zip_path = os.path.join(prod_base, f"{board['zip_prefix']}_Gerbers.zip")
    if os.path.exists(gerber_zip_path): os.remove(gerber_zip_path)
    with zipfile.ZipFile(gerber_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in sorted(os.listdir(gerber_dir)):
            full_path = os.path.join(gerber_dir, file)
            zipf.write(full_path, file)
    print(f"  -> Clean Gerber ZIP (JLCPCB Ready): {gerber_zip_path} ({os.path.getsize(gerber_zip_path)} bytes)")

    assembly_zip_path = os.path.join(prod_base, f"{board['zip_prefix']}_Assembly_SMT.zip")
    if os.path.exists(assembly_zip_path): os.remove(assembly_zip_path)
    with zipfile.ZipFile(assembly_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in sorted(os.listdir(assembly_dir)):
            full_path = os.path.join(assembly_dir, file)
            zipf.write(full_path, file)
    print(f"  -> SMT Assembly ZIP: {assembly_zip_path} ({os.path.getsize(assembly_zip_path)} bytes)")

def sync_to_onedrive():
    print("\n========================================================")
    print("  Synchronizing Production folder with OneDrive Master")
    print("========================================================")
    src = os.path.join(PROJECT_ROOT, "production")
    dst = os.path.join(ONEDRIVE_ROOT, "production")
    os.makedirs(dst, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"[+] All production packages synchronized to: {dst}")

def main():
    for board in BOARDS:
        create_board_package(board)
    sync_to_onedrive()
    print("\n[SUCCESS] 100% JLCPCB Compliant Production Packages Generated!")

if __name__ == '__main__':
    main()
