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

doc1_uuid = "b20a3201-2001-4001-8001-000000000002"
doc2_uuid = "b20a3201-2001-4001-8001-000000000003"
doc3_uuid = "b20a3201-2001-4001-8001-000000000004"
doc4_uuid = "b20a3201-2001-4001-8001-000000000005"

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

print("Costruzione completa dei 4 fogli gerarchici...")
