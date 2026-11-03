import os
import sys

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts"
sys.path.append(scripts_dir)
from symbol_helper import extract_symbol

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
root_uuid = "b20a3201-1001-4001-8001-000000000001"
sheet1_uuid = "b20a3201-1001-4001-8001-000000000002"
doc1_uuid = "b20a3201-2001-4001-8001-000000000002"

def make_inst(ref, sheet_u, doc_u, unit=1):
    return f"""    (instances
      (project "FDD-Test-Board"
        (path "/{root_uuid}/{sheet_u}"
          (reference "{ref}") (unit {unit})
        )
        (path "/{doc_u}"
          (reference "{ref}") (unit {unit})
        )
      )
    )"""

# Estraiamo i simboli esatti da KiCad 9
sym_gnd = extract_symbol("power", "GND")
sym_pwrflag = extract_symbol("power", "PWR_FLAG")
sym_conn2 = extract_symbol("Connector", "Conn_01x02_Pin")
sym_conn4 = extract_symbol("Connector", "Conn_01x04_Pin")
sym_r = extract_symbol("Device", "R")
sym_c = extract_symbol("Device", "C")
sym_cp = extract_symbol("Device", "C_Polarized")
sym_l = extract_symbol("Device", "L")
sym_tps = extract_symbol("Regulator_Switching", "TPS54302")
sym_ina = extract_symbol("Amplifier_Current", "INA180A1")
sym_pmos = extract_symbol("Transistor_FET", "AO3401A")
sym_npn = extract_symbol("Transistor_BJT", "2N3904")

lib_symbols_s1 = f"""  (lib_symbols
{sym_gnd}
{sym_pwrflag}
{sym_conn2}
{sym_conn4}
{sym_r}
{sym_c}
{sym_cp}
{sym_l}
{sym_tps}
{sym_ina}
{sym_pmos}
{sym_npn}
  )"""

print("Simboli estratti con successo per Foglio 1!")
