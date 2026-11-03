import os
import sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"
sys.path.append(scripts_dir)
from symbol_helper import extract_symbol

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
root_uuid = "b20a3201-1001-4001-8001-000000000001"
sheet1_uuid = "b20a3201-1001-4001-8001-000000000002"
sheet2_uuid = "b20a3201-1001-4001-8001-000000000003"
sheet3_uuid = "b20a3201-1001-4001-8001-000000000004"
sheet4_uuid = "b20a3201-1001-4001-8001-000000000005"

print("Avvio generazione suite schematica KiCad 9.0...")
