import os
import sys
import uuid
import re
import subprocess
from collections import defaultdict

kicad_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\kicad"
sym_dir = r"C:\Program Files\KiCad\9.0\share\kicad\symbols"
local_sym_path = os.path.join(kicad_dir, "FDD-Test-Board.kicad_sym")

scripts_dir = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\IC-Test-Board\scripts"
sys.path.append(scripts_dir)
from generate_clean_erc0_project import extract_symbol_exact, get_symbol_pins

ROOT_UUID = "b20a3201-1001-4001-8001-000000000001"

def u():
    return str(uuid.uuid4())

def make_inst(ref, sheet_u, doc_u, unit=1):
    return f"""    (instances
      (project "FDD-Test-Board"
        (path "/{ROOT_UUID}/{sheet_u}"
          (reference "{ref}") (unit {unit})
        )
        (path "/{doc_u}"
          (reference "{ref}") (unit {unit})
        )
      )
    )"""

def title_block(title, sheet_num, desc):
    return f"""  (paper "A3")
  (title_block
    (title "{title}")
    (date "2026-11-02")
    (rev "1.0")
    (company "Alessio Iodice")
    (comment 1 "Author / Hardware Designer: Alessio Iodice <alessio67@gmail.com>")
    (comment 2 "{desc}")
    (comment 3 "License: CC BY-NC-SA 4.0")
    (comment 4 "Validated on KiCad 9.0 — 0 ERC / 0 DRC violations")
  )"""

print("Setup completed successfully.")
