import os, re

script_path = r"C:\Users\aless\OneDrive\temp\Manutenzione\Kicad_Project\FDD_Tester\scripts\build_zero_erc_fdd.py"

with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace make_instances_block
old_inst = """def make_instances_block(ref, sheet_uuid, doc_uuid, unit=1, sheet_stem=""):
    return f\"\"\"    (instances
      (project "FDD-Test-Board"
        (path "/{ROOT_UUID}/{sheet_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
        (path "/{doc_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
      )
      (project "{sheet_stem}"
        (path "/{doc_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
      )
    )\"\"\""""

new_inst = """def make_instances_block(ref, sheet_uuid, doc_uuid, unit=1, sheet_stem=""):
    return f\"\"\"    (instances
      (project "FDD-Test-Board"
        (path "/{ROOT_UUID}/{sheet_uuid}"
          (reference "{ref}")
          (unit {unit})
        )
      )
    )\"\"\""""

assert old_inst in text, "old_inst pattern not found!"
text = text.replace(old_inst, new_inst)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated make_instances_block in build_zero_erc_fdd.py!")
